#!/bin/bash
# Explicitly invoked maintenance; never launched by either camera service.
set -euo pipefail
test "$(id -u)" -eq 0
test "$(hostname)" = ProMichAiCam1
backup="/var/backups/promich-camera/$(date -u +%Y%m%dT%H%M%SZ)-maintenance"
install -d -m 700 "$backup"
dpkg-query -W > "$backup/packages-before.txt"
unit_dir=/etc/systemd/system/NetworkManager-wait-online.service.d
if [ -d "$unit_dir" ]; then cp -a "$unit_dir" "$backup/wait-online-before"; fi
printf 'BACKUP=%s\n' "$backup"
# Preserve both networks and their priority. The recorded failed association
# takes ~75 seconds; a 60-second wait service incorrectly fails during failover.
install -d "$unit_dir"
printf '[Service]\nEnvironment=NM_ONLINE_TIMEOUT=120\n' > "$unit_dir/90-promich-timeout.conf"
systemctl daemon-reload
systemctl restart NetworkManager-wait-online.service
systemctl is-active NetworkManager-wait-online.service
printf 'NETWORK_WAIT_OK\n'
apt-get update
apt-get --simulate --no-remove upgrade > "$backup/upgrade-plan.txt"
apt-get -y --no-remove -o Dpkg::Options::=--force-confold upgrade
dpkg --audit
dpkg-query -W > "$backup/packages-after.txt"
printf 'MAINTENANCE_OK\n'
