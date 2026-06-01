# Homelab DevOps

This repository contains the applications and Kubernetes manifests for my personal **DevOps homelab**. Apps are containerised with Docker, pushed to **Docker Hub**, and deployed to a **locally-hosted Kubernetes cluster** running on **Proxmox** (1 master + 2 workers) via **GitHub Actions**.

## Applications

| App | Stack | Local URL |
|-----|-------|-----------|
| [Flask Portfolio](flask_app_portfolio/) | Flask + SQLite + Gunicorn | http://localhost:5004 |
| [Zen E-Commerce](zen_ecommerce/) | FastAPI + Next.js + PostgreSQL | http://localhost:3000 |

## Homelab Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────────────────┐
│  GitHub     │────▶│  Docker Hub │────▶│  Kubernetes on Proxmox      │
│  Actions    │     │  Registry   │     │  (1 master + 2 workers)     │
└─────────────┘     └─────────────┘     └─────────────────────────────┘
```

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

## CI/CD

Each app has its own GitHub Actions workflow that:
1. Builds the Docker image(s)
2. Pushes to Docker Hub
3. Updates the Kubernetes manifest image tags
4. Commits the updated manifests back to the repo

Deploy to the cluster by applying the manifests:
```bash
kubectl apply -f k8s-apps/<app-name>/
```

## Author

**Zaid Lazim**
- GitHub: [github.com/zaidlaz](https://github.com/zaidlaz)
- LinkedIn: [linkedin.com/in/zaidlaz](https://www.linkedin.com/in/zaidlaz)
