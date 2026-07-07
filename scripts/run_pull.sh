#!/usr/bin/env bash
# run from cron, e.g.
#   15 6 * * *  /opt/campaign-pulse/scripts/run_pull.sh >> /var/log/campaign-pulse.log 2>&1
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; source .env; set +a
.venv/bin/python -m pulse.pull --days 3
