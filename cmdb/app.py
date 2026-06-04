import os
from kubernetes import client, config
from datetime import date, datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
DB_USER = os.getenv("DB_USER", "cmdbuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "cmdbpassword")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "homelab_cmdb")
app.config["SQLALCHEMY_DATABASE_URI"] = (
f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(50))
    asset_type = db.Column(db.String(50), nullable=False)
    operating_system = db.Column(db.String(100))
    cpu = db.Column(db.String(100))
    memory_gb = db.Column(db.Integer)
    disk_gb = db.Column(db.Integer)
    status = db.Column(db.String(30), default="Unknown")
    owner = db.Column(db.String(100), default="viduka")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(50))
    hostname = db.Column(db.String(100))
    port = db.Column(db.Integer)
    protocol = db.Column(db.String(20), default="HTTP")
    status = db.Column(db.String(30), default="Unknown")

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(255), nullable=False)
    target = db.Column(db.String(255))
    provider = db.Column(db.String(50), default="Internal DNS")
    public_access = db.Column(db.Boolean, default=False)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(255), nullable=False)
    issuer = db.Column(db.String(100))
    expiry_date = db.Column(db.Date)

    @property
    def days_remaining(self):
        if not self.expiry_date:
            return None
        return (self.expiry_date - date.today()).days

def seed_data():
    if Asset.query.first():
        return
    db.session.add_all([
        Asset(hostname="pve", ip_address="192.168.13.6", asset_type="Proxmox", operating_system="Proxmox VE", 
status="Running", owner="viduka"),
        Asset(hostname="mgmt01", ip_address="192.168.13.210", asset_type="VM", operating_system="Ubuntu Server", 
status="Running", owner="viduka"),
        Asset(hostname="k8-master", ip_address="192.168.13.32", asset_type="Kubernetes Node", 
operating_system="Ubuntu Server", status="Healthy", owner="viduka"),
        Asset(hostname="k8-wk1", ip_address="192.168.13.3", asset_type="Kubernetes Node", 
operating_system="Ubuntu Server", status="Healthy", owner="viduka"),
        Asset(hostname="k8-wk2", ip_address="192.168.13.25", asset_type="Kubernetes Node", 
operating_system="Ubuntu Server", status="Healthy", owner="viduka"),
        Asset(hostname="k8-wk3", ip_address="192.168.13.215", asset_type="Kubernetes Node", 
operating_system="Ubuntu Server", status="Healthy", owner="viduka"),
    ])
    db.session.add_all([
        Service(service_name="Grafana", service_type="Monitoring", hostname="grafana.lab", port=3000, 
protocol="HTTPS", status="UP"),

  Service(service_name="Prometheus", service_type="Monitoring", hostname="prometheus.lab", port=9090, 
protocol="HTTP", status="UP"),
        Service(service_name="Uptime Kuma", service_type="Monitoring", hostname="192.168.13.210", port=3001, 
protocol="HTTP", status="UP"),
        Service(service_name="Recipe App", service_type="Application", hostname="recipe.zaidlaz.uk", port=443, 
protocol="HTTPS", status="UP"),
        Service(service_name="Portfolio App", service_type="Application", hostname="portfolio.zaidlaz.uk", 
port=443, protocol="HTTPS", status="UP"),
    ])
    db.session.add_all([
        Domain(domain_name="cmdb.lab", target="192.168.13.240", provider="Internal DNS", public_access=False), 
        Domain(domain_name="recipe.zaidlaz.uk", target="Cloudflare Tunnel", provider="Cloudflare", 
public_access=True),
        Domain(domain_name="portfolio.zaidlaz.uk", target="Cloudflare Tunnel", provider="Cloudflare", 
public_access=True),
        Domain(domain_name="grafana.lab", target="192.168.13.240", provider="Internal DNS", public_access=False), 
        Domain(domain_name="argocd.lab", target="192.168.13.240", provider="Internal DNS", public_access=False), 
    ])
    db.session.add_all([
        Certificate(domain_name="cmdb.lab", issuer="homelab-ca-issuer", expiry_date=date(2027, 6, 1)), 
        Certificate(domain_name="recipe.zaidlaz.uk", issuer="Cloudflare/Let's Encrypt", expiry_date=date(2026, 9, 
1)),
        Certificate(domain_name="portfolio.zaidlaz.uk", issuer="Cloudflare/Let's Encrypt", expiry_date=date(2026, 
9, 1)),
    ])
    db.session.commit()

def discover_kubernetes():
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()

    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    networking_v1 = client.NetworkingV1Api()

    discovered = []

    for node in v1.list_node().items:
        discovered.append({
            "hostname": node.metadata.name,
            "ip_address": next(
                (addr.address for addr in node.status.addresses if addr.type == "InternalIP"),
                "N/A"
            ),
            "asset_type": "Kubernetes Node",
            "status": "Ready"
        })

    for ns in v1.list_namespace().items:
        discovered.append({
            "hostname": ns.metadata.name,
            "ip_address": "N/A",
            "asset_type": "Kubernetes Namespace",
            "status": ns.status.phase
        })

    return discovered

@app.before_request
def init_database():
    db.create_all()
    seed_data()


@app.route("/discover/kubernetes")
def discover_k8s():
    items = discover_kubernetes()

    for item in items:
        existing = Asset.query.filter_by(hostname=item["hostname"]).first()

        if not existing:
            asset = Asset(
                hostname=item["hostname"],
                ip_address=item["ip_address"],
                asset_type=item["asset_type"],
                status=item["status"]
            )
            db.session.add(asset)

    db.session.commit()

    return redirect(url_for("assets"))

@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        asset_count=Asset.query.count(),
        service_count=Service.query.count(),
        domain_count=Domain.query.count(),
        cert_count=Certificate.query.count(),
        now=datetime.utcnow(),
    )

@app.route("/assets", methods=["GET", "POST"])
def assets():
    if request.method == "POST":
        db.session.add(Asset(
            hostname=request.form["hostname"],
            ip_address=request.form.get("ip_address"),
            asset_type=request.form["asset_type"],
            operating_system=request.form.get("operating_system"),
            status=request.form.get("status", "Unknown"),
            owner=request.form.get("owner", "viduka"),
        ))
        db.session.commit()
        return redirect(url_for("assets"))
    return render_template("assets.html", assets=Asset.query.order_by(Asset.hostname).all()) 

@app.route("/services")
def services():
    return render_template("services.html", services=Service.query.order_by(Service.service_name).all()) 

@app.route("/domains")
def domains():
    return render_template("domains.html", domains=Domain.query.order_by(Domain.domain_name).all())

@app.route("/certificates")
def certificates():
    return render_template(
        "certificates.html",
        certificates=Certificate.query.order_by(Certificate.domain_name).all()
)

@app.route("/health")
def health():
    return {"status": "ok", "service": "cmdb"}

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

