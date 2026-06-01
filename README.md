# Homelab DevOps

This repository contains the applications and Kubernetes manifests for my personal **DevOps homelab**. Apps are containerised with Docker, pushed to **Docker Hub** by **GitHub Actions**, and continuously deployed to a **locally-hosted Kubernetes cluster** running on **Proxmox** (1 master + 2 workers) via **Argo CD** (GitOps).

## Applications

| App | Stack | Local URL |
|-----|-------|-----------|
| [Flask Portfolio](flask_app_portfolio/) | Flask + SQLite + Gunicorn | http://localhost:5004 |
| [Zen E-Commerce](zen_ecommerce/) | FastAPI + Next.js + PostgreSQL | http://localhost:3000 |

## Homelab Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────────────────┐
│  GitHub     │────▶│  Docker Hub │────▶│  Kubernetes on Proxmox       │
│  Actions    │     │  Registry   │     │  (1 master + 2 workers)     │
└─────────────┘     └─────────────┘     │                             │
                                        │      ┌──────────┐         │
                                        │      │ Argo CD  │◀────────┘
                                        │      │ (GitOps) │         │
                                        │      └──────────┘         │
                                        └─────────────────────────────┘
```

- **GitHub Actions** builds images and updates manifest tags
- **Argo CD** watches the repo and syncs manifests to the cluster automatically
- **Docker Hub** hosts the container images

## Repository Structure

```
.
├── flask_app_portfolio/      # Flask portfolio app (source + Docker)
├── zen_ecommerce/            # Full-stack e-commerce app (source + Docker)
├── k8s-apps/                 # Kubernetes manifests
│   ├── demo-app/
│   ├── flask_app_portfolio/
│   └── zen_ecommerce/
└── .github/workflows/        # CI/CD pipelines
```

## CI/CD & GitOps

### GitHub Actions
Each app has its own workflow that:
1. Builds the Docker image(s)
2. Pushes them to Docker Hub
3. Updates the Kubernetes manifest image tags
4. Commits the updated manifests back to the repo

### Argo CD (GitOps)
**Argo CD** is installed on the Kubernetes cluster and watches this repository. When GitHub Actions commits new image tags, Argo CD automatically detects the change and syncs the updated manifests to the cluster.

Deploy an app by creating an Argo CD Application:
```bash
argocd app create zen-ecommerce \
  --repo https://github.com/zaidlaz/homelab-devops-apps.git \
  --path k8s-apps/zen_ecommerce \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace zen-ecommerce \
  --sync-policy automated
```

> **Note:** Secrets (e.g., `zen-ecommerce-secrets`) must be created manually on the cluster before syncing, as they are excluded from the repo for security.

## Author

**Zaid Lazim**
- GitHub: [github.com/zaidlaz](https://github.com/zaidlaz)
- LinkedIn: [linkedin.com/in/zaidlaz](https://www.linkedin.com/in/zaidlaz)
