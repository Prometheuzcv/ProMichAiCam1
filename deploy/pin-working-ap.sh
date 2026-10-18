#!/bin/bash
# Run as root with a verified connection name and working AP BSSID.
# Private network configuration and backups must stay on the device.
set -euo pipefail
test "$(id -u)" -eq 0
test "$(hostname)" = ProMichAiCam1
test "$#" -eq 2
python3 -c 'import yaml'
profile=$1
bssid=${2^^}
[[ $bssid =~ ^([0-9A-F]{2}:){5}[0-9A-F]{2}$ ]]
test "$(nmcli -g GENERAL.CONNECTION device show wlan0)" = "$profile"
nmcli -t -f IN-USE,BSSID device wifi list --rescan no | grep -Fqx "*:${bssid//:/\\:}"
backup="/var/backups/promich-camera/$(date -u +%Y%m%dT%H%M%SZ)-ap-pin"
install -d -m 700 "$backup"
cp -a /etc/netplan "$backup/"
cp -a /etc/NetworkManager/system-connections "$backup/"
nmcli --escape no -g 802-11-wireless.bssid connection show "$profile" > "$backup/previous-bssid"
nmcli connection modify "$profile" 802-11-wireless.bssid "$bssid"
test "$(nmcli --escape no -g 802-11-wireless.bssid connection show "$profile")" = "$bssid"
# NetworkManager's Netplan backend must have persisted the pin, not just
# changed the in-memory connection or its generated file under /run.
python3 - "$bssid" <<'PY'
import pathlib, sys, yaml
target = sys.argv[1].upper()
found = False
for path in pathlib.Path('/etc/netplan').glob('*.yaml'):
    data = yaml.safe_load(path.read_text()) or {}
    for wifi in data.get('network', {}).get('wifis', {}).values():
        for ap in wifi.get('access-points', {}).values():
            found |= str(ap.get('bssid', '')).upper() == target
assert found, 'BSSID pin was not persisted in Netplan'
PY
printf 'BACKUP=%s\nAP_PIN_PERSISTED\n' "$backup"
# The live connection is left active; a separately verified restart tests boot.
