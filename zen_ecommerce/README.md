# Zen E-Commerce

A full-stack electronics e-commerce platform built with **FastAPI**, **Next.js**, and **PostgreSQL** for my **DevOps homelab**. It is containerised with Docker and deployed to a **Kubernetes cluster (1 master + 2 workers) running on Proxmox** via **GitHub Actions** and **Docker Hub**.

## Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15 (React 18 + TypeScript + Bootstrap 5) |
| Backend | FastAPI (Python 3.12+) + SQLAlchemy + Uvicorn |
| Database | PostgreSQL 16 |
| Local Dev | Docker Compose |
| CI/CD | GitHub Actions |
| Registry | Docker Hub |
| Deployment | Kubernetes (raw manifests) |

## Prerequisites

- Docker & Docker Compose
- Node.js 20 LTS (for local frontend dev)
- Python 3.12+ (for local backend dev)
- A Kubernetes cluster on **Proxmox** — **1 master + 2 worker nodes**
- `kubectl` configured to talk to your cluster
- Git

## Run locally (Docker Compose)

```bash
cd zen_ecommerce
cp .env.example .env
docker compose up --build
```

The app will be available at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000

Test health endpoints:
```bash
curl http://localhost:8000/health   # {"status":"ok"}
curl http://localhost:8000/ready    # {"status":"ready"}
curl http://localhost:3000/api/health  # {"status":"ok"}
```

## Deploy to Kubernetes

### 1. GitHub Actions CI/CD

The workflow (`.github/workflows/zen-ecommerce.yml`) automatically:
1. Builds Docker images for the backend and frontend
2. Pushes them to **Docker Hub**
3. Updates the image tags in the Kubernetes manifests
4. Commits the updated manifests back to the repo

**Required repository secrets:**
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

Trigger a deployment by pushing to `main` or run the workflow manually from the **Actions** tab.

### 2. Apply to your local cluster

After the workflow commits the updated manifests:

```bash
# From the repo root
kubectl apply -f k8s-apps/zen_ecommerce/
```

> **Note:** Create the required secrets manually before applying. The database credentials are stored in `postgres-secret` and the application secrets in `zen-ecommerce-secrets`:
> ```bash
> # Create the namespace first
> kubectl create namespace zen-ecommerce
>
> # Database secret (used by the postgres StatefulSet)
> kubectl create secret generic postgres-secret \
>   --namespace zen-ecommerce \
>   --from-literal=POSTGRES_DB='ecommerce_db' \
>   --from-literal=POSTGRES_USER='ecom_user' \
>   --from-literal=POSTGRES_PASSWORD='<your-db-password>'
>
> # Application secret (used by the backend Deployment)
> kubectl create secret generic zen-ecommerce-secrets \
>   --namespace zen-ecommerce \
>   --from-literal=db-password='<your-db-password>' \
>   --from-literal=admin-password='<your-admin-password>'
> ```
>
> The database runs as a **StatefulSet** with a 10Gi PVC using the `local-path` storage class. The backend connects via individual environment variables (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) rather than a single `DATABASE_URL`.

## Repo structure

```
zen_ecommerce/
├── src/
│   ├── backend/          FastAPI backend (models, auth, API routes)
│   └── frontend/         Next.js frontend (React + TypeScript)
├── docker-compose.yml    Local orchestration
├── .env.example          Environment variable template
└── README.md

.github/workflows/        GitHub Actions CI/CD
k8s-apps/zen_ecommerce/     Kubernetes manifests
```
