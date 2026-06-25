#!/usr/bin/env bash
set -euo pipefail
IMAGE="${IMAGE:-zaid/linux-kb:latest}"
docker build -t "$IMAGE" .
docker push "$IMAGE"
echo "Pushed $IMAGE"
