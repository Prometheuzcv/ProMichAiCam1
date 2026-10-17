#!/usr/bin/env python3
"""Run the dedicated camera kiosk after its local HTTP server is reachable."""
import os
import json
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

URL = 'http://127.0.0.1:8080/display'


def main():
    runtime = Path(os.environ.get('XDG_RUNTIME_DIR', f'/run/user/{os.getuid()}'))
    display = os.environ.get('WAYLAND_DISPLAY', 'wayland-0')
    while not (runtime / display).exists():
        time.sleep(1)
    while True:
        try:
            with urllib.request.urlopen(URL, timeout=3) as response:
                if response.status == 200:
                    break
        except (OSError, urllib.error.URLError):
            pass
        time.sleep(1)
    profile = Path.home() / '.local/state/promich-camera/chromium'
    profile.mkdir(parents=True, exist_ok=True)
    preferences = profile / 'Default/Preferences'
    preferences.parent.mkdir(parents=True, exist_ok=True)
    settings = json.loads(preferences.read_text()) if preferences.exists() else {}
    settings.setdefault('translate', {})['enabled'] = False
    settings.setdefault('intl', {})['accept_languages'] = 'cs,en'
    temporary = preferences.with_suffix('.promich-tmp')
    temporary.write_text(json.dumps(settings), encoding='utf-8')
    temporary.replace(preferences)
    env = os.environ.copy()
    env['XDG_RUNTIME_DIR'] = str(runtime)
    env['WAYLAND_DISPLAY'] = display
    raise SystemExit(subprocess.call([
        '/usr/bin/chromium', '--ozone-platform=wayland', '--kiosk',
        '--no-first-run', '--no-default-browser-check', '--noerrdialogs',
        '--password-store=basic', '--disable-extensions',
        '--disable-features=Translate', '--lang=cs',
        '--disable-session-crashed-bubble', '--autoplay-policy=no-user-gesture-required',
        '--user-data-dir=' + str(profile), URL,
    ], env=env))


if __name__ == '__main__':
    main()
