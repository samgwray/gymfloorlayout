#!/usr/bin/env bash
# Ship this repository to the gymfloorlayout.com server and rebuild the containers there:
#   GYMFLOORLAYOUT_HOST=user@your-server deploy/deploy.sh
# Needs the server's SSH key at ~/.ssh/gymfloorlayout.pem and SSH access from this network
set -euo pipefail

HOST="${GYMFLOORLAYOUT_HOST:?Set GYMFLOORLAYOUT_HOST to your SSH user@host}"
KEY="${GYMFLOORLAYOUT_KEY:-$HOME/.ssh/gymfloorlayout.pem}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SSH="ssh -i $KEY -o StrictHostKeyChecking=accept-new"

rsync -az --delete -e "$SSH" \
  --exclude node_modules --exclude .next --exclude .venv --exclude __pycache__ \
  --exclude .pytest_cache --exclude .mypy_cache --exclude .ruff_cache --exclude '*.tsbuildinfo' \
  "$ROOT/backend" "$ROOT/frontend" "$ROOT/data" "$ROOT/deploy" "$ROOT/.dockerignore" \
  "$HOST:/opt/gymfloorlayout/"
$SSH "$HOST" 'cd /opt/gymfloorlayout/deploy \
  && docker compose up -d --build --remove-orphans \
  && docker compose exec -T caddy caddy reload --config /etc/caddy/Caddyfile \
  && docker image prune -f'
