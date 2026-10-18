#!/bin/bash
set -euo pipefail
test "$(id -u)" -eq 0
test "$(hostname)" = ProMichAiCam1
test "$#" -eq 2
source_dir=$(cd -- "$(dirname -- "$0")" && pwd)
backup="/var/backups/promich-camera/$(date -u +%Y%m%dT%H%M%SZ)-wifi-supervisor"
install -d -m 700 "$backup"
for file in /etc/promich-camera/wifi-supervisor.json \
    /usr/local/libexec/promich-wifi-supervisor.py \
    /etc/systemd/system/promich-wifi-supervisor.service \
    /etc/systemd/system/promich-wifi-supervisor.timer \
    /etc/NetworkManager/conf.d/99-promich-diagnostics.conf; do
    if [ -f "$file" ]; then cp -p "$file" "$backup/$(basename "$file")"; fi
done
install -d -m 700 /etc/promich-camera
# Read only non-secret fields. Profiles, stored passwords and priorities stay intact.
python3 - "$1" "$2" <<'PY'
import json, os, pathlib, re, subprocess, sys
def field(uuid, key):
    return subprocess.check_output(['nmcli', '--escape', 'no', '-g', key,
                                    'connection', 'show', 'uuid', uuid], text=True).strip()
profiles = []
for uuid in sys.argv[1:]:
    assert re.fullmatch(r'[0-9a-fA-F-]{36}', uuid)
    assert field(uuid, 'connection.type') == '802-11-wireless'
    assert field(uuid, 'connection.autoconnect') == 'yes'
    assert field(uuid, '802-11-wireless-security.psk-flags').startswith('0')
    profiles.append({'uuid': uuid, 'ssid': field(uuid, '802-11-wireless.ssid'),
                     'bssid': field(uuid, '802-11-wireless.bssid')})
assert profiles[0]['uuid'] != profiles[1]['uuid']
path = pathlib.Path('/etc/promich-camera/wifi-supervisor.json')
path.write_text(json.dumps({'profiles': profiles}))
os.chmod(path, 0o600)
PY
install -d /usr/local/libexec
install -m 755 "$source_dir/wifi-supervisor.py" /usr/local/libexec/promich-wifi-supervisor.py
install -m 644 "$source_dir/promich-wifi-supervisor.service" /etc/systemd/system/
install -m 644 "$source_dir/promich-wifi-supervisor.timer" /etc/systemd/system/
systemd-analyze verify /etc/systemd/system/promich-wifi-supervisor.service /etc/systemd/system/promich-wifi-supervisor.timer
# The failure evidence is preserved; stop verbose temporary NM logging.
if [ -f /etc/NetworkManager/conf.d/99-promich-diagnostics.conf ]; then
    printf '[logging]\nlevel=INFO\ndomains=DEFAULT\n' > /etc/NetworkManager/conf.d/99-promich-diagnostics.conf
    nmcli general logging level INFO domains DEFAULT
fi
systemctl daemon-reload
systemctl enable --now promich-wifi-supervisor.timer
systemctl start promich-wifi-supervisor.service
printf 'BACKUP=%s\nWIFI_SUPERVISOR_INSTALLED\n' "$backup"
