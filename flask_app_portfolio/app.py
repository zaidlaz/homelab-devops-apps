import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "comments.db")

os.makedirs(INSTANCE_DIR, exist_ok=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

PROFILE = {
    "name": "Zaid Lazim",
    "job_title": "Python, Linux & Cloud & DevOps Enthusiast",
    "linkedin": "https://www.linkedin.com/in/zaidlaz",
    "email": "lazimzaid@yahoo.com.sg",
    "github": "https://zaidlaz.github.io/github.io/",
    "summary": (
        "I am building hands-on skills in Python, Linux administration, and DevOps. "
        "My work includes Flask applications, Bash automation, cron scheduling, "
        "troubleshooting, and practical infrastructure projects."
    ),
    "about": (
        "I enjoy creating practical technical solutions that improve automation, "
        "visibility, and system reliability. My interests include Python scripting, "
        "Flask development, Linux operations, SQLite, backup automation, monitoring "
        "dashboards, and deployment workflows."
    ),
    "skills": [
        "Python scripting",
        "Flask web development",
        "Linux administration",
        "Bash scripting",
        "Cron job automation",
        "SQLite database integration",
        "System monitoring",
        "Troubleshooting and log analysis",
    ],
    "projects": [
             {
            "title": "Built and deployed a cloud-native e-commerce platform using FastAPI, Docker, and Azure Container Apps, integrated with Neon serverless PostgreSQL for scalable and cost-efficient data storage.",
            "repo_url": "https://github.com/zaidlaz/zen-ecommerce",
            "description": [
                "Designed RESTful backend with SQLAlchemy ORM and Jinja2 templating",
                "Implemented full e-commerce flow: product catalog, cart, checkout, and order management",
                "Developed admin dashboard with CRUD operations for product management",
                "Containerized application using Docker and deployed via Azure Container Apps",
                "Integrated CI/CD pipeline using GitHub Actions for automated build and deployment",
                "Optimized infrastructure cost by replacing managed DB with serverless PostgreSQL (Neon)",
                ],
        },
        {
            "title": "Enterprise DevOps Homelab Platform",
            "repo_url": "https://github.com/zaidlaz/homelab-devops-mgmt",
            "video_url": "https://youtu.be/OKY7_zPGjRg",
            "description": [
               "Designed and built a production-inspired DevOps homelab on a GMKTec Mini PC running Proxmox VE",
               "Provisioned and managed Kubernetes infrastructure with dedicated control plane and worker nodes",
               "Implemented GitOps deployment workflows using ArgoCD and GitHub repositories",
               "Automated infrastructure provisioning using Terraform and Infrastructure as Code principles",
               "Secured public services using Cloudflare Tunnel and private administration through Tailscale Zero Trust networking",
               "Deployed observability stack using Prometheus, Grafana, Node Exporter and cAdvisor",
               "Hosted multiple production-style applications including Portfolio Website, CMDB Platform and Recipe Manager",
               "Created a complete architecture walkthrough video demonstrating enterprise infrastructure concepts",
               ],
        },
        {
            "title": "Flask Portfolio Website",
            "repo_url": "https://dev.azure.com/ZaidB/_git/flask-app-portfolio",
            "description": "A personal portfolio site with login, registration, and guestbook commenting using Python, Flask, SQLite, and Flask-Login running on Azure AKS cluster using Azure CICD pipeline and Azure Repo",
        },
        {
            "title": "Flask Recipe Manager",
            "repo_url": "https://github.com/zaidlaz/homelab-devops-apps/tree/main/my_recipe",
            "description": "A beautiful, feature-rich Flask web application for managing your recipe collections. Create, organize, search, and share recipes with an intuitive web interface.", 
        },
        {
            "title": "Server Health Dashboard",
            "repo_url": "https://github.com/zaidlaz/grafana-prometheus-homelab-monitoring",
            "description": "A docker container running grafana and prometheus showing CPU, memory, disk, and network usage of several vms in my homelab",
        },
        {
            "title": "HomeLab Operations CMDB",
            "repo_url": "https://github.com/zaidlaz/homelab-devops-apps/tree/main/cmdb",
            "description": "A lightweight Configuration Management Database (CMDB) for tracking homelab infrastructure assets, services, domains, and SSL certificates. Built with Flask and PostgreSQL, it includes an automatic Kubernetes discovery feature that reads cluster nodes and namespaces via the Kubernetes API",
        },
        {
            "title": "Advanced Linux Server Performance & Troubleshooting",
            "repo_url": "https://github.com/zaidlaz/linux-server-performance-troubleshooting",
            "description": "A field manual for production Linux performance engineering, covers kernel internals, hardware counters and root-cause methodologies.",
        },
    ]
}



class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    comments = db.relationship("Comment", backref="author", lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        return str(self.id)


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/")
def home():
    return render_template("home.html", profile=PROFILE, page_title="Home")


@app.route("/about/")
def about():
    return render_template("about.html", profile=PROFILE, page_title="About")


@app.route("/projects/")
def projects():
    return render_template("projects.html", profile=PROFILE, page_title="Projects")


@app.route("/guestbook/", methods=["GET", "POST"])
@login_required
def guestbook():
    if request.method == "POST":
        content = request.form.get("contents", "").strip()

        if not content:
            flash("Comment cannot be empty.")
            return redirect(url_for("guestbook"))

        if len(content) > 4096:
            flash("Comment is too long.")
            return redirect(url_for("guestbook"))

        comment = Comment(content=content, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()

        flash("Comment posted successfully.")
        return redirect(url_for("guestbook"))

    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template(
        "guestbook.html",
        profile=PROFILE,
        page_title="Guestbook",
        comments=comments,
        timestamp=datetime.now(),
    )


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template(
            "register.html",
            profile=PROFILE,
            page_title="Register",
            error=None,
        )

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not username or not password or not confirm_password:
        return render_template(
            "register.html",
            profile=PROFILE,
            page_title="Register",
            error="All fields are required.",
        )

    if password != confirm_password:
        return render_template(
            "register.html",
            profile=PROFILE,
            page_title="Register",
            error="Passwords do not match.",
        )

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return render_template(
            "register.html",
            profile=PROFILE,
            page_title="Register",
            error="Username already exists.",
        )

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful. Please log in.")
    return redirect(url_for("login"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template(
            "login.html",
            profile=PROFILE,
            page_title="Login",
            error=None,
        )

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return render_template(
            "login.html",
            profile=PROFILE,
            page_title="Login",
            error="Invalid username or password.",
        )

    login_user(user)
    flash("You are now logged in.")
    return redirect(url_for("guestbook"))


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("home"))


@app.route("/health/")
def health():
    return {"status": "ok"}, 200


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=False)
