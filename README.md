# homelab-devops-apps
# Flask App Portfolio Deployment Documentation

## Overview

This document describes the complete deployment process for the Flask Portfolio application using:

- Proxmox VE
- Ubuntu VMs
- Kubernetes Cluster
- ArgoCD GitOps
- Docker Hub
- GitHub
- Flask Application

It also documents all major issues encountered and their resolutions.

---

# Architecture Overview

```text
VS Code (ubuntu-dev01)
        ↓
Git Push
        ↓
GitHub Repository
        ↓
Docker Build
        ↓
Docker Hub Registry
        ↓
ArgoCD GitOps
        ↓
Kubernetes Cluster
        ↓
Flask Portfolio Application
```

---

# Environment Details

## Infrastructure

| Component | IP Address | Purpose |
|---|---|---|
| Proxmox Host | 192.168.13.6 | Hypervisor |
| mgmt01 | 192.168.13.210 | Management / Ansible / kubectl |
| k8-master-homelab | 192.168.13.211 | Kubernetes Control Plane |
| k8-wk1-homelab | 192.168.13.212 | Kubernetes Worker |
| k8-wk2-homelab | 192.168.13.213 | Kubernetes Worker |
| devops-tools | 192.168.13.214 | CI/CD and tooling |

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Proxmox VE | Virtualization |
| Terraform | VM provisioning |
| Cloud-init | VM customization |
| Ansible | Kubernetes deployment |
| Kubernetes | Container orchestration |
| Calico | Pod networking |
| ArgoCD | GitOps deployment |
| Docker | Containerization |
| Docker Hub | Container registry |
| GitHub | Source control |
| Flask | Python web application |

---

# Phase 1 — Flask Application Creation

## Application Structure

```text
homelab-devops/
├── flask_app_portfolio/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── k8s-apps/
    └── flask_app_portfolio/
        ├── deployment.yaml
        └── service.yaml
```

---

## app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask Portfolio App running on Kubernetes via ArgoCD!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## requirements.txt

```text
flask
```

---

## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

# Phase 2 — Docker Hub Setup

## Docker Hub Repository

Repository Name:

```text
zaid/flask-app-portfolio
```

Visibility:

```text
Public
```

---

## Docker Hub Token

Created a Docker Hub Personal Access Token with:

```text
Read
Write
Delete
```

---

# Phase 3 — Docker Build and Push

## Login to Docker Hub

```bash
docker login
```

Username:

```text
zaid
```

Password:

```text
Docker Hub Access Token
```

---

## Build Docker Image

```bash
docker build -t zaid/flask-app-portfolio:latest ./flask_app_portfolio
```

---

## Push Docker Image

```bash
docker push zaid/flask-app-portfolio:latest
```

---

# Phase 4 — Kubernetes Deployment

## deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app-portfolio
  namespace: flask-app-portfolio
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app-portfolio
  template:
    metadata:
      labels:
        app: flask-app-portfolio
    spec:
      containers:
        - name: flask-app-portfolio
          image: zaid/flask-app-portfolio:latest
          ports:
            - containerPort: 5004
```

---

## service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-portfolio-service
  namespace: flask-app-portfolio
spec:
  type: NodePort
  selector:
    app: flask-app-portfolio
  ports:
    - port: 5004
      targetPort: 5004
      nodePort: 30081
```

---

# Phase 5 — Namespace Creation

```bash
kubectl create namespace flask-app-portfolio
```

---

# Phase 6 — ArgoCD Application

## Create Application

```bash
kubectl apply -f - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: flask-app-portfolio
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/zaidlaz/homelab-devops-apps.git
    targetRevision: main
    path: k8s-apps/flask_app_portfolio
  destination:
    server: https://kubernetes.default.svc
    namespace: flask-app-portfolio
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
```

---

# Validation Commands

## Check ArgoCD Application

```bash
kubectl get applications -n argocd
```

Expected:

```text
SYNC STATUS: Synced
HEALTH STATUS: Healthy
```

---

## Check Pods

```bash
kubectl get pods -n flask-app-portfolio -o wide
```

Expected:

```text
STATUS: Running
```

---

## Check Service

```bash
kubectl get svc -n flask-app-portfolio
```

Expected:

```text
NodePort: 30081
```

---

## Access Application

```text
http://192.168.13.212:30081
```

or

```text
http://192.168.13.213:30081
```

---

# Issues Encountered and Resolutions

# Issue 1 — ArgoCD Application Path Does Not Exist

## Error

```text
app path does not exist
```

## Root Cause

Incorrect Git repository path configured in ArgoCD.

Configured path:

```text
k8s-apps/flask-app-portfolio
```

Actual path:

```text
k8s-apps/flask_app_portfolio
```

## Resolution

Updated ArgoCD Application path:

```bash
kubectl patch application flask-app-portfolio -n argocd --type merge -p '{"spec":{"source":{"path":"k8s-apps/flask_app_portfolio"}}}'
```

---

# Issue 2 — Docker Push Access Denied

## Error

```text
push access denied
```

## Root Cause

Incorrect Docker Hub authentication.

Also:

- Repository did not exist initially
- Wrong Docker username used

## Resolution

1. Created Docker Hub repository
2. Created Docker Hub access token
3. Logged in correctly:

```bash
docker login
```

4. Used correct image name:

```text
zaid/flask-app-portfolio
```

---

# Issue 3 — Docker Permission Denied

## Error

```text
permission denied while trying to connect to docker.sock
```

## Root Cause

User was not in docker group.

## Resolution

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

---

# Issue 4 — Kubernetes ImagePullBackOff

## Error

```text
ImagePullBackOff
```

## Root Cause

Docker image did not exist in Docker Hub.

## Resolution

Built and pushed image manually:

```bash
docker build -t zaid/flask-app-portfolio:latest ./flask_app_portfolio

docker push zaid/flask-app-portfolio:latest
```

---

# Issue 5 — NodePort Not Reachable

## Symptoms

```text
curl failed to connect
```

## Root Cause

Container application listened on port:

```text
5004
```

But Kubernetes Service targeted:

```text
5000
```

## Resolution

Updated:

### deployment.yaml

```yaml
containerPort: 5004
```

### service.yaml

```yaml
port: 5004
targetPort: 5004
```

---

# Issue 6 — Internal Service Connectivity Failure

## Error

```text
Could not connect to server
```

## Root Cause

Mismatch between application listening port and Kubernetes service target port.

## Resolution

Aligned all ports to:

```text
5004
```

---

# Useful Troubleshooting Commands

## Check ArgoCD

```bash
kubectl describe application flask-app-portfolio -n argocd
```

---

## Check Pod Logs

```bash
kubectl logs -n flask-app-portfolio deployment/flask-app-portfolio
```

---

## Check Service Endpoints

```bash
kubectl get endpoints -n flask-app-portfolio
```

---

## Test Inside Kubernetes

```bash
kubectl run test-curl --rm -it --image=curlimages/curl -- sh
```

Inside pod:

```sh
curl http://flask-app-portfolio-service.flask-app-portfolio.svc.cluster.local:5004
```

---

## Restart Deployment

```bash
kubectl rollout restart deployment/flask-app-portfolio -n flask-app-portfolio
```

---

# Final Working Architecture

```text
Developer (VS Code)
        ↓
GitHub Repository
        ↓
Docker Build
        ↓
Docker Hub Registry
        ↓
ArgoCD GitOps Sync
        ↓
Kubernetes Cluster
        ↓
Flask Portfolio App
```

---

# Final Outcome

Successfully implemented:

- Proxmox homelab
- Terraform VM provisioning
- Cloud-init VM customization
- Kubernetes cluster
- Calico networking
- ArgoCD GitOps
- Docker image management
- Flask containerized application
- GitOps deployment pipeline
- Kubernetes service exposure
- End-to-end DevOps workflow

---

# Future Improvements

Potential next enhancements:

1. Ingress Controller
2. HTTPS with cert-manager
3. GitHub Actions CI/CD
4. Monitoring with Prometheus and Grafana
5. Centralized logging
6. Helm charts
7. ArgoCD ApplicationSets
8. Private container registry
9. Horizontal Pod Autoscaler
10. Persistent storage

