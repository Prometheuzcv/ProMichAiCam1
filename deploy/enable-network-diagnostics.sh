#!/bin/bash
# Preserve evidence across a failed boot; does not reconnect or restart Wi-Fi.
set -euo pipefail
test "$(id -u)" -eq 0
test "$(hostname)" = ProMichAiCam1
backup="/var/backups/promich-camera/$(date -u +%Y%m%dT%H%M%SZ)-network-diagnostics"
install -d -m 700 "$backup"
journal_conf=/etc/systemd/journald.conf.d/99-promich-diagnostics.conf
network_conf=/etc/NetworkManager/conf.d/99-promich-diagnostics.conf
for config in "$journal_conf" "$network_conf"; do
    if [ -f "$config" ]; then cp -p "$config" "$backup/$(basename "$(dirname "$config")")-$(basename "$config")"; fi
done
install -d /etc/systemd/journald.conf.d /etc/NetworkManager/conf.d
cat > "$journal_conf" <<'EOF'
[Journal]
Storage=persistent
SystemMaxUse=64M
SystemMaxFileSize=8M
SystemKeepFree=512M
RuntimeMaxUse=16M
MaxRetentionSec=7day
Compress=yes
EOF
cat > "$network_conf" <<'EOF'
[logging]
level=DEBUG
domains=CORE,DEVICE,WIFI,SUPPLICANT,IP4,DHCP4
EOF
systemctl restart systemd-journald
journalctl --flush
nmcli general logging level DEBUG domains CORE,DEVICE,WIFI,SUPPLICANT,IP4,DHCP4
printf 'BACKUP=%s\n' "$backup"
systemd-analyze cat-config systemd/journald.conf | grep -E '^Storage=|^SystemMaxUse=|^RuntimeMaxUse='
nmcli general logging
journalctl --disk-usage
printf 'NETWORK_DIAGNOSTICS_READY\n'
