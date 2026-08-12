#!/usr/bin/env bash
set -euo pipefail

KB_ROOT="$HOME/projects/homelab-devops/linux-kb-gitops"

cd "$KB_ROOT"

echo "[1/6] Creating Kubernetes folders..."

mkdir -p docs/kubernetes/troubleshooting
mkdir -p docs/kubernetes/operations
mkdir -p docs/kubernetes/architecture
mkdir -p docs/kubernetes/cheatsheet
mkdir -p docs/kubernetes/case-studies

echo "[2/6] Creating Kubernetes dashboard..."

cat > docs/kubernetes/index.md <<'EOF'
# Kubernetes Operations Runbooks

Kubernetes troubleshooting notes, operational procedures, and production-style runbooks.

## Common Troubleshooting Topics

<div class="grid cards" markdown>

- **Pod Not Starting**

    Pending pods, scheduling failures, taints, resources, and PVC issues.

    [Open Runbook](troubleshooting/pod-not-starting.md)

- **ImagePullBackOff**

    Wrong image, wrong tag, private registry, Docker Hub rate limit, and pull secrets.

    [Open Runbook](troubleshooting/imagepullbackoff.md)

- **CrashLoopBackOff**

    Application crash, bad config, missing secrets, failed probes, and OOMKilled.

    [Open Runbook](troubleshooting/crashloopbackoff.md)

- **Service Unreachable**

    Service selector mismatch, wrong targetPort, endpoints missing, and DNS issues.

    [Open Runbook](troubleshooting/service-unreachable.md)

- **Ingress Routing Issue**

    Traefik routing, host mismatch, backend service issue, 404, and 502 errors.

    [Open Runbook](troubleshooting/ingress-routing.md)

- **ConfigMap and Secret Issues**

    Missing environment variables, incorrect mounts, stale config, and restart requirements.

    [Open Runbook](troubleshooting/configmap-secret.md)

</div>

---

## Kubernetes Troubleshooting Flow

<div class="mermaid">
flowchart LR
    A([Kubernetes Issue]) --> B{Pod Status?}
    B --> C[Pending]
    B --> D[ImagePullBackOff]
    B --> E[CrashLoopBackOff]
    B --> F[Running but Unreachable]

    C --> C1[Check Scheduler, Nodes, PVC, Taints]
    D --> D1[Check Image, Registry, Tag, Pull Secret]
    E --> E1[Check Logs, Previous Logs, Probes, Config]
    F --> F1[Check Service, Endpoints, Ingress, DNS]

    C1 --> G([Resolution])
    D1 --> G
    E1 --> G
    F1 --> G
</div>

---

## Quick Commands

| Purpose | Command |
|---|---|
| All Pods | `kubectl get pods -A` |
| Describe Pod | `kubectl describe pod <pod> -n <namespace>` |
| Logs | `kubectl logs <pod> -n <namespace>` |
| Previous Logs | `kubectl logs <pod> -n <namespace> --previous` |
| Events | `kubectl get events -A --sort-by=.lastTimestamp` |
| Services | `kubectl get svc -A` |
| Endpoints | `kubectl get endpoints -A` |
| Ingress | `kubectl get ingress -A` |
| Nodes | `kubectl get nodes -o wide` |
| Resource Usage | `kubectl top pods -A` |

EOF

echo "[3/6] Creating troubleshooting runbooks..."

cat > docs/kubernetes/troubleshooting/pod-not-starting.md <<'EOF'
# Pod Not Starting

## Symptoms

- Pod remains in `Pending`
- Pod is not scheduled to any node
- Deployment shows unavailable replicas

## Investigation Steps

### 1. Check pod status

```bash
kubectl get pods -n <namespace> -o wide
