#!/usr/bin/env bash
set -euo pipefail
IMAGE="zaid/linux-kb:local"
docker build -t "$IMAGE" .
docker rm -f linux-kb-test >/dev/null 2>&1 || true
docker run -d --name linux-kb-test -p 8088:80 "$IMAGE"
echo "Open: http://localhost:8088"
