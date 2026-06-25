# Linux KB GitOps

A searchable Linux Operations Knowledge Base built with MkDocs Material and deployed to Kubernetes using Argo CD.

## Quick Start

```bash
./scripts/01-test-local-docker.sh
./scripts/02-build-push.sh
./scripts/03-deploy-argocd-app.sh
```

Default settings:

- App directory: `linux-kb-gitops`
- Docker image: `zaid/linux-kb:latest`
- Git repo: `https://github.com/zaid/homelab-devops.git`
- Argo CD app path: `linux-kb-gitops/k8s`
- Hostname: `kb.zaidlaz.uk`
- Ingress class: `traefik`

Edit Markdown files under `docs/`, then rebuild and push the image.
