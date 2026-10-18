#!/usr/bin/python3
"""Retry two saved Wi-Fi profiles and cautiously prefer stronger signal."""
import json
import os
from pathlib import Path
import subprocess
import time

SCAN_INTERVAL = 300
SWITCH_COOLDOWN = 900
MIN_SIGNAL = 60
SIGNAL_MARGIN = 20


def parse_access_points(output):
    rows, row = [], {}
    for line in output.splitlines():
        key, sep, value = line.partition(':')
        if not sep:
            continue
        if key == 'IN-USE':
            row = {}
        row[key] = value.strip()
        if key == 'SIGNAL':
            try:
                row['SIGNAL'] = int(row['SIGNAL'])
                rows.append(row)
            except ValueError:
                pass
    return rows


def plan(profiles, state, now, device_state, current_uuid, aps=None):
    """Return one UUID to activate, or None. Mutate only supervisor state."""
    if device_state == 100:
        # Never replace a connection outside the two explicitly configured ones.
        if current_uuid not in [p['uuid'] for p in profiles] or aps is None:
            return None
        current = next((ap for ap in aps if ap.get('IN-USE') == '*'), None)
        candidates = []
        for profile in profiles:
            if profile['uuid'] == current_uuid:
                continue
            matches = [ap for ap in aps
                       if ap.get('SSID') == profile['ssid']
                       and (not profile['bssid'] or
                            ap.get('BSSID', '').upper() == profile['bssid'].upper())]
            if matches:
                candidates.append((max(ap['SIGNAL'] for ap in matches), profile['uuid']))
        best = max(candidates, default=(0, None))
        if (not current or best[0] < MIN_SIGNAL
                or best[0] - current['SIGNAL'] < SIGNAL_MARGIN
                or now - state.get('last_switch', -SWITCH_COOLDOWN) < SWITCH_COOLDOWN):
            state.pop('candidate', None)
            state.pop('confirmations', None)
            return None
        state['confirmations'] = (state.get('confirmations', 0) + 1
                                  if state.get('candidate') == best[1] else 1)
        state['candidate'] = best[1]
        if state['confirmations'] < 2:
            return None
        state.update(last_switch=now, fallback=current_uuid)
        state.pop('candidate', None)
        state.pop('confirmations', None)
        return best[1]
    # Let NetworkManager finish its own association, authentication and DHCP.
    if device_state not in (30, 120):
        return None
    state.pop('candidate', None)
    state.pop('confirmations', None)
    fallback = state.pop('fallback', None)
    if fallback:
        return fallback
    index = state.get('next', 0) % len(profiles)
    state['next'] = (index + 1) % len(profiles)
    return profiles[index]['uuid']


def nmcli(*args):
    return subprocess.run(['/usr/bin/nmcli', *args], text=True,
                          capture_output=True, timeout=35, check=True).stdout.strip()


def main():
    config = json.loads(Path('/etc/promich-camera/wifi-supervisor.json').read_text())
    profiles = config['profiles']
    if len(profiles) != 2 or profiles[0]['uuid'] == profiles[1]['uuid']:
        raise ValueError('Exactly two different saved profiles are required')
    state_path = Path('/var/lib/promich-wifi-supervisor/state.json')
    boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
    try:
        state = json.loads(state_path.read_text())
    except (FileNotFoundError, ValueError):
        state = {}
    if state.get('boot') != boot:
        state = {'boot': boot}
    now = time.monotonic()
    status = nmcli('-g', 'GENERAL.STATE', 'device', 'show', 'wlan0')
    device_state = int(status.split()[0])
    current_uuid = nmcli('-g', 'GENERAL.CON-UUID', 'device', 'show', 'wlan0')
    aps = None
    if device_state == 100:
        if now - state.get('last_scan', -SCAN_INTERVAL) < SCAN_INTERVAL:
            return
        aps = parse_access_points(nmcli('-w', '20', '-m', 'multiline', '-f',
                                        'IN-USE,SSID,BSSID,SIGNAL', 'device',
                                        'wifi', 'list', 'ifname', 'wlan0', '--rescan', 'yes'))
        state['last_scan'] = now
        # Recheck after scanning: do not act on a connection that already changed.
        if nmcli('-g', 'GENERAL.CON-UUID', 'device', 'show', 'wlan0') != current_uuid:
            return
    target = plan(profiles, state, now, device_state, current_uuid, aps)
    temporary = state_path.with_suffix('.tmp')
    temporary.write_text(json.dumps(state))
    os.chmod(temporary, 0o600)
    temporary.replace(state_path)
    if target:
        # Asynchronous activation: NetworkManager remains the only Wi-Fi manager.
        # Explicit activation also retries profiles blocked after no-secrets.
        nmcli('-w', '0', 'connection', 'up', 'uuid', target, 'ifname', 'wlan0')
        print('WIFI_ACTIVATION_REQUESTED', flush=True)


if __name__ == '__main__':
    main()
