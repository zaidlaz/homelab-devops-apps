#!/usr/bin/env bash
set -euo pipefail
kubectl apply -f argocd/linux-kb-application.yaml
kubectl get application linux-kb -n argocd
