# HomeLab CMDB

A lightweight **Configuration Management Database (CMDB)** for tracking homelab infrastructure assets, services, domains, and SSL certificates. Built with **Flask** and **PostgreSQL**, it includes an automatic **Kubernetes discovery** feature that reads cluster nodes and namespaces via the Kubernetes API.

## Features

- **Asset Management** — Track physical and virtual infrastructure (Proxmox hosts, VMs, Kubernetes nodes, etc.)
- **Asset Deletion** — Remove hosts/assets from the CMDB via a confirmation-protected delete action
- **Service Registry** — Monitor internal and external services with hostname, port, protocol, and status
- **Domain Inventory** — Record DNS mappings, providers, and public/private access flags
- **Certificate Tracking** — Log SSL/TLS certificates with expiry dates and automatic "days remaining" calculation
- **Kubernetes Discovery** — One-click discovery of cluster nodes and namespaces via in-cluster ServiceAccount
- **Professional Dark UI** — Modern glassmorphism dashboard with dark slate theme, Bootstrap 5, Bootstrap Icons, Inter font, and smooth animations
- **Health Endpoint** — `/health` for Kubernetes liveness/readiness probes

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, Flask 3.x, Flask-SQLAlchemy |
| Database | PostgreSQL 16 |
| K8s Client | `kubernetes` Python SDK |
| Server | Gunicorn |
| Frontend | Jinja2 templates, Bootstrap 5, Bootstrap Icons, Inter font, custom dark theme CSS |
| Container | Docker (python:3.12-slim) |
| Orchestration | Kubernetes (raw manifests) |
| Ingress | Traefik |

## Data Models

### Asset
| Field | Type | Description |
|-------|------|-------------|
| hostname | String(100) | Unique identifier |
| ip_address | String(50) | IPv4/IPv6 address |
| asset_type | String(50) | e.g. VM, Proxmox, Kubernetes Node |
| operating_system | String(100) | OS name/version |
| cpu | String(100) | CPU details |
| memory_gb | Integer | RAM in GB |
| disk_gb | Integer | Disk in GB |
| status | String(30) | Running, Healthy, Unknown, etc. |
| owner | String(100) | Default: `viduka` |

### Service
| Field | Type | Description |
|-------|------|-------------|
| service_name | String(100) | e.g. Grafana, Prometheus |
| service_type | String(50) | Monitoring, Application, etc. |
| hostname | String(100) | DNS or IP |
| port | Integer | Service port |
| protocol | String(20) | HTTP, HTTPS, TCP |
| status | String(30) | UP, DOWN, Unknown |

### Domain
| Field | Type | Description |
|-------|------|-------------|
| domain_name | String(255) | FQDN |
| target | String(255) | IP or tunnel endpoint |
| provider | String(50) | Internal DNS, Cloudflare |
| public_access | Boolean | Exposed to internet? |

### Certificate
| Field | Type | Description |
|-------|------|-------------|
| domain_name | String(255) | Associated domain |
| issuer | String(100) | CA or provider |
| expiry_date | Date | Expiration date |
| days_remaining | Property | Computed from expiry_date |

## Project Structure

```
cmdb/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image build
├── .gitignore              # Excludes secrets, venv, and local DBs from Git
├── static/
│   └── style.css           # Custom styles
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── assets.html
│   ├── services.html
│   ├── domains.html
│   └── certificates.html
└── docs/
    └── screenshots/          # UI preview images
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_USER` | `cmdbuser` | PostgreSQL username |
| `DB_PASSWORD` | `cmdbpassword` | PostgreSQL password |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_NAME` | `homelab_cmdb` | PostgreSQL database name |

## Local Development

```bash
cd cmdb

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up local PostgreSQL or use Docker Compose
export DB_HOST=localhost
export DB_USER=cmdbuser
export DB_PASSWORD=cmdbpassword
export DB_NAME=homelab_cmdb

# Run the application
python app.py
```

The app will be available at `http://localhost:5000`.

## Docker

```bash
# Build image
docker build -t homelab-cmdb:latest ./cmdb

# Run container
docker run -p 5000:5000 \
  -e DB_HOST=your-db-host \
  -e DB_USER=cmdbuser \
  -e DB_PASSWORD=cmdbpassword \
  -e DB_NAME=homelab_cmdb \
  homelab-cmdb:latest
```

## Kubernetes Deployment

The CMDB is deployed to the homelab Kubernetes cluster with the following components:

| Resource | File | Purpose |
|----------|------|---------|
| Namespace | `namespace.yaml` | Isolates CMDB resources |
| Secret | `postgres-secret.yaml` | PostgreSQL credentials |
| PVC | `postgres-pvc.yaml` | Persistent storage for PostgreSQL |
| Deployment (DB) | `postgres-deployment.yaml` | PostgreSQL 16 instance |
| Service (DB) | `postgres-service.yaml` | Cluster-internal DB access |
| ServiceAccount + RBAC | `cmdb-rbac.yaml` | K8s API read permissions |
| Deployment (App) | `cmdb-deployment.yaml` | Flask/Gunicorn application |
| Service (App) | `cmdb-service.yaml` | Exposes app on port 80 |
| Ingress | `ingress.yaml` | Routes `cmdb.lab` to the app |

### Kubernetes Discovery RBAC

The app uses a dedicated `ServiceAccount` (`cmdb-sa`) with a `ClusterRole` granting read-only access to:
- Nodes, Namespaces, Pods, Services
- Deployments, ReplicaSets
- Ingresses

This allows the `/discover/kubernetes` endpoint to auto-populate the asset database.

## CI/CD

The GitHub Actions workflow (`.github/workflows/cmdb-docker-build.yml`) automatically:
1. Builds the Docker image on changes to `cmdb/**`
2. Pushes to Docker Hub (`zaid/homelab-cmdb`)
3. Updates the Kubernetes manifest image tag
4. Commits the updated manifest back to the repo

Argo CD then detects the change and syncs the deployment automatically.

## UI / UX

The CMDB features a **modern dark-themed dashboard** designed for infrastructure monitoring:

- **Dark Slate Theme** — Gradient background (`#0f172a` → `#1e293b`) with high-contrast text
- **Glassmorphism Cards** — Frosted glass effect with subtle borders and shadows
- **Color-Coded Categories** — Each entity type has a unique accent color:
  - Assets: Blue (`#38bdf8`)
  - Services: Green (`#34d399`)
  - Domains: Amber (`#fbbf24`)
  - Certificates: Pink (`#f472b6`)
- **Status Badges** — Semantic colors for Running, Down, Warning, and Unknown states
- **Bootstrap Icons** — Contextual icons on every page for visual clarity
- **Inter Font** — Clean, modern typography from Google Fonts
- **Smooth Animations** — Fade-in effects and hover transitions on cards and buttons
- **Responsive Layout** — Mobile-friendly navbar with collapsible menu

## Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Dashboard with counts |
| `/assets` | GET, POST | List and add assets |
| `/assets/<id>/delete` | POST | Delete an asset (with confirmation) |
| `/services` | GET | List services |
| `/domains` | GET | List domains |
| `/certificates` | GET | List certificates |
| `/discover/kubernetes` | GET | Auto-discover K8s nodes/namespaces |
| `/health` | GET | Health check JSON |

## Seed Data

On first startup, the database is automatically seeded with:
- **Assets**: Proxmox host, management VM, and all Kubernetes worker nodes
- **Services**: Grafana, Prometheus, Uptime Kuma, Recipe App, Portfolio App
- **Domains**: Internal (`*.lab`) and public (`*.zaidlaz.uk`) domains
- **Certificates**: Homelab CA and Cloudflare/Let's Encrypt certs

## Dashboard Preview

![CMDB Dashboard](/cmdb/docs/screenshots/cmdb-dashboard.png)

## Author

**Zaid Lazim**
- GitHub: [github.com/zaidlaz](https://github.com/zaidlaz)
- LinkedIn: [linkedin.com/in/zaidlaz](https://www.linkedin.com/in/zaidlaz)
