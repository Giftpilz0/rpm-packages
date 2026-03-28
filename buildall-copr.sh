#!/bin/bash

BASE="https://copr.fedorainfracloud.org/webhooks/custom/$COPR_WEBHOOK_ID/$COPR_WEBHOOK_UUID"

declare -A BUILD_LEVELS=(
    [1]="cpptrace"
    [2]="eww-git matugen-git niri-git quickshell-git waypipe-git yolk-git"
    [3]=""
    [4]=""
)

WAIT_TIME=240

echo "Starting Copr builds with dependency levels..."

for level in {1..4}; do
    packages="${BUILD_LEVELS[$level]}"

    if [[ -z "$packages" ]]; then
        continue
    fi

    echo -e "\n=== Level $level ==="
    for pkg in $packages; do
        (curl -X POST "$BASE/$pkg/" > /dev/null 2>&1 && echo "✓ $pkg") &
    done
    wait

    if [[ $level -lt 4 ]]; then
        echo "Waiting ${WAIT_TIME}s for Level $level builds to complete..."
        sleep "$WAIT_TIME"
    fi
done

echo -e "\n=== All builds triggered ==="
