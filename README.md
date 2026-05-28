# 🚀 DevOps Homelab on Proxmox

Enterprise-style DevOps / Platform Engineering homelab running on Proxmox VE with Kubernetes, GitOps, CI/CD, Monitoring, Ingress, and Secure Remote Access.

---

# 📌 Overview

This project simulates a modern cloud-native enterprise infrastructure environment using:

* Proxmox VE
* Terraform
* Cloud-Init
* Ansible
* Kubernetes
* ArgoCD GitOps
* GitHub Actions CI/CD
* Docker Hub
* Flask Portfolio Application
* Prometheus + Grafana Monitoring
* MetalLB Load Balancing
* Traefik Ingress Controller
* cert-manager Internal PKI
* Tailscale Secure Remote Access

The goal of this homelab is to gain hands-on experience with real-world Platform Engineering and DevOps workflows.

---

# 🏗️ Current Architecture

```text
Developer Laptop
       │
       ▼
GitHub Repository
       │
       ▼
GitHub Actions CI/CD
       │
       ▼
Docker Hub Registry
       │
       ▼
ArgoCD GitOps
       │
       ▼
Kubernetes Cluster
       │
 ┌─────┼─────────────┐
 ▼     ▼             ▼
Flask  Grafana     ArgoCD
App
       │
       ▼
Traefik Ingress
       │
       ▼
MetalLB LoadBalancer
       │
       ▼
Tailscale Secure Access
```

---

# 🖥️ Infrastructure

| Component  | Details          |
| ---------- | ---------------- |
| Hypervisor | Proxmox VE 9.2.2 |
| Hardware   | GMKTec Mini PC   |
| CPU        | Intel i5-13500H  |
| RAM        | 32GB             |
| Storage    | 1TB SSD          |
| OS         | Ubuntu 24.04     |

---

# 🧩 VM Layout

| VM Name           | IP Address     | Purpose                  |
| ----------------- | -------------- | ------------------------ |
| Proxmox Host      | 192.168.13.6   | Hypervisor               |
| mgmt01            | 192.168.13.210 | kubectl / Ansible / Helm |
| k8-master-homelab | 192.168.13.211 | Kubernetes Control Plane |
| k8-wk1-homelab    | 192.168.13.212 | Kubernetes Worker        |
| k8-wk2-homelab    | 192.168.13.213 | Kubernetes Worker        |
| devops-tools      | 192.168.13.214 | Future tooling/services  |

---

# ☸️ Kubernetes Stack

## Core Components

* Kubernetes v1.30.x
* containerd
* kubeadm
* Calico CNI
* CoreDNS

## GitOps

* ArgoCD
* Auto-sync enabled
* Self-heal enabled

## Networking

* MetalLB
* Traefik Ingress Controller
* Internal DNS routing

## Monitoring

* Prometheus
* Grafana
* Alertmanager
* node-exporter
* kube-state-metrics

## Security

* cert-manager
* Internal Root CA
* Trusted HTTPS certificates
* Tailscale remote access

---

# 🔄 CI/CD Pipeline

GitHub Actions automatically:

1. Builds Docker image
2. Pushes image to Docker Hub
3. Updates Kubernetes manifests
4. Triggers ArgoCD sync
5. Deploys rolling updates to Kubernetes

---

# 🐳 Docker Image

```text
zaid/flask-app-portfolio
```

---

# 📂 Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── flask-app-portfolio.yml
│
├── flask_app_portfolio/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   └── static/
│
├── k8s-apps/
│   └── flask_app_portfolio/
│       ├── deployment.yaml
│       └── service.yaml
│
├── ingress/
│   ├── flask-portfolio-ingress.yaml
│   ├── argocd-ingress.yaml
│   └── grafana-ingress.yaml
│
├── cert-manager/
│   ├── portfolio-certificate.yaml
│   ├── argocd-certificate.yaml
│   └── grafana-certificate.yaml
│
├── terraform/
│   ├── main.tf
│   ├── provider.tf
│   └── variables.tf
│
└── README.md
```

---

# 🌐 Current Service URLs

| Service         | URL                       |
| --------------- | ------------------------- |
| Flask Portfolio | https://portfolio.lab     |
| ArgoCD          | https://argocd.lab        |
| Grafana         | https://grafana.lab       |
| Proxmox VE      | https://192.168.13.6:8006 |

---

# 🔐 Internal PKI

This homelab uses:

* cert-manager
* Internal Root CA
* Trusted TLS certificates

This removes browser certificate warnings for internal `.lab` domains.

---

# 🛠️ Key Technologies

| Category          | Technologies         |
| ----------------- | -------------------- |
| Virtualization    | Proxmox VE           |
| IaC               | Terraform            |
| Config Management | Ansible              |
| Container Runtime | containerd           |
| Orchestration     | Kubernetes           |
| GitOps            | ArgoCD               |
| CI/CD             | GitHub Actions       |
| Registry          | Docker Hub           |
| Monitoring        | Prometheus + Grafana |
| Ingress           | Traefik              |
| Load Balancing    | MetalLB              |
| Remote Access     | Tailscale            |
| TLS               | cert-manager         |

---

# 📈 Future Enhancements

Planned improvements:

* Longhorn distributed storage
* Loki centralized logging
* Velero Kubernetes backups
* Tailscale Kubernetes Operator
* ExternalDNS
* SSO with Keycloak/Authentik
* Harbor private registry
* Trivy security scanning
* Kubernetes HA control plane

---

# 📚 Key Learning Outcomes

This homelab provides practical experience in:

* Infrastructure-as-Code
* Kubernetes administration
* GitOps workflows
* CI/CD automation
* Cloud-native networking
* Kubernetes ingress
* TLS certificate management
* Monitoring & observability
* Production-style platform engineering

---

# 👨‍💻 Author

**Zaid Lazim**

* Linux, Cloud & DevOps Enthusiast
* Platform Engineering Homelab Builder
* Kubernetes & Automation Learner

GitHub:

```text
https://github.com/zaidlaz
```

LinkedIn:

```text
https://www.linkedin.com/in/zaidlaz
```

---

# ⭐ Acknowledgements

This project was built as part of an ongoing hands-on DevOps and Platform Engineering learning journey using open-source technologies and enterprise-inspired architecture.
