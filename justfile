set shell := ["bash", "-euo", "pipefail", "-c"]

# List recipes
default:
    @just --list --unsorted

# Run all linters and formatters (pre-commit); CI runs this too
lint *args:
    pre-commit run --all-files {{args}}

# Definition of done
check: lint

# Build all packages locally with mock
build:
    ./buildall-local.sh

# Trigger Copr builds (needs COPR_WEBHOOK_ID and COPR_WEBHOOK_UUID)
deploy:
    ./buildall-copr.sh

# Bump spec versions to the latest upstream releases/commits
update:
    ./update.sh
