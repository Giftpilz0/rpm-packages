#!/usr/bin/env bash
set -euo pipefail

BASE="https://copr.fedorainfracloud.org/webhooks/custom/$COPR_WEBHOOK_ID/$COPR_WEBHOOK_UUID"

declare -A BUILD_LEVELS=(
    [1]="cpptrace"
    [2]="eww-git matugen-git niri-git quickshell-git waypipe-git yolk-git"
)

WAIT_TIME=240

echo "Starting Copr builds with dependency levels..."

for level in 1 2; do
    packages="${BUILD_LEVELS[$level]}"

    echo -e "\n=== Level $level ==="
    for pkg in $packages; do
        (curl -fsS -X POST "$BASE/$pkg/" > /dev/null && echo "✓ $pkg") &
    done
    wait

    if [[ $level -lt 2 ]]; then
        echo "Waiting ${WAIT_TIME}s for Level $level builds to complete..."
        sleep "$WAIT_TIME"
    fi
done

echo -e "\n=== All builds triggered ==="
