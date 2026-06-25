# Easy Deployment Procedure

This version does not require local Python or `pip install`.

## 1. Test locally with Docker

```bash
cd linux-kb-gitops
./scripts/01-test-local-docker.sh
```

Open:

```text
http://localhost:8088
```

## 2. Build and push image

```bash
./scripts/02-build-push.sh
```

Default image:

```text
zaid/linux-kb:latest
```

## 3. Commit to Git

```bash
git add linux-kb-gitops
git commit -m "Add Linux KB GitOps app"
git push
```

## 4. Create Argo CD application

```bash
./scripts/03-deploy-argocd-app.sh
```

## 5. Check status

```bash
kubectl get applications -n argocd
kubectl get pods -n linux-kb -o wide
kubectl get ingress -n linux-kb
```

## 6. Test inside cluster

```bash
kubectl port-forward -n linux-kb svc/linux-kb 8080:80
```

Open:

```text
http://localhost:8080
```

## 7. Website URL

```text
http://kb.zaidlaz.uk
```
