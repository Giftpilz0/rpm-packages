#!/usr/bin/env bash
set -euo pipefail

BASE="https://copr.fedorainfracloud.org/webhooks/custom/$COPR_WEBHOOK_ID/$COPR_WEBHOOK_UUID"

packages="matugen-git niri-git waypipe-git"

echo "Starting Copr builds..."

for pkg in $packages; do
    (curl -fsS -X POST "$BASE/$pkg/" > /dev/null && echo "✓ $pkg") &
done
wait

echo -e "\n=== All builds triggered ==="
