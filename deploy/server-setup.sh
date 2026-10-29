#!/bin/bash
# One-time setup of the gymfloorlayout.com server (Amazon Linux 2023, arm64): Docker with current
# Compose and Buildx plugins, rsync, and 2 GiB of swap for builds. Safe to run again.
#   ssh -i ~/.ssh/gymfloorlayout.pem ec2-user@<server> 'sudo bash -s' < deploy/server-setup.sh
set -euxo pipefail
dnf install -y docker rsync
systemctl enable --now docker
usermod -aG docker ec2-user
plugins=/usr/local/lib/docker/cli-plugins
mkdir -p "$plugins"
curl -fsSL -o "$plugins/docker-compose" \
  https://github.com/docker/compose/releases/latest/download/docker-compose-linux-aarch64
release=$(curl -fsSL https://api.github.com/repos/docker/buildx/releases/latest)
buildx=$(printf '%s\n' "$release" | sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p' | head -n 1)
curl -fsSL -o "$plugins/docker-buildx" \
  "https://github.com/docker/buildx/releases/download/${buildx}/buildx-${buildx}.linux-arm64"
chmod +x "$plugins/docker-compose" "$plugins/docker-buildx"
if [ ! -f /swapfile ]; then
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
fi
swapon --show | grep -q /swapfile || swapon /swapfile
grep -q '^/swapfile ' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
mkdir -p /opt/gymfloorlayout
chown ec2-user:ec2-user /opt/gymfloorlayout
