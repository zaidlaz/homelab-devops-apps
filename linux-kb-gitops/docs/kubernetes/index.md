# Kubernetes Operations Runbook

Kubernetes troubleshooting notes, operational procedures, and homelab case studies.

## Common Troubleshooting Topics

<div class="grid cards" markdown>

- **Pod Not Starting**

    Pending pods, scheduling failures, node issues, and PVC problems.

    [Open Runbook](troubleshooting/pod-not-starting.md)

- **ImagePullBackOff**

    Wrong image, wrong tag, private registry, and Docker Hub pull errors.

    [Open Runbook](troubleshooting/imagepullbackoff.md)

- **CrashLoopBackOff**

    Application crash, missing config, bad command, OOMKilled, and probe failures.

    [Open Runbook](troubleshooting/crashloopbackoff.md)

- **Service Unreachable**

    Service selector, endpoints, targetPort, DNS, and NetworkPolicy issues.

    [Open Runbook](troubleshooting/service-unreachable.md)

- **Ingress Routing Issue**

    Traefik, host header, service backend, 404, 502, and Cloudflare Tunnel issues.

    [Open Runbook](troubleshooting/ingress-routing.md)

- **ConfigMap and Secret Issues**

    Missing config, wrong environment values, secret decoding, and restart handling.

    [Open Runbook](troubleshooting/configmap-secret.md)

</div>
