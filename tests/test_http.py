"""Exercise the real HTTP handler without opening the physical camera."""
import importlib.util
from pathlib import Path
import sys
import threading
import types
import urllib.request

sys.modules['cv2'] = types.ModuleType('cv2')
picamera = types.ModuleType('picamera2')
picamera.Picamera2 = object
sys.modules['picamera2'] = picamera
devices = types.ModuleType('picamera2.devices')
devices.IMX500 = object
sys.modules['picamera2.devices'] = devices
path = Path(__file__).resolve().parents[1] / 'app.py'
spec = importlib.util.spec_from_file_location('camera_http', path)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
server = app.ThreadingHTTPServer(('127.0.0.1', 0), app.Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = 'http://127.0.0.1:' + str(server.server_port)
try:
    with urllib.request.urlopen(base + '/display') as response:
        content = response.read().decode()
        assert 'object-fit:contain' in content
        assert 'contextmenu' in content
        assert 'AbortSignal.timeout' in content
        assert response.headers['Content-Type'].startswith('text/html')
    with urllib.request.urlopen(base + '/') as response:
        assert 'Rozpoznané objekty' in response.read().decode()
    with urllib.request.urlopen(base + '/status') as response:
        assert b'"ready": false' in response.read()
    app.frame = b'\xff\xd8test-frame\xff\xd9'
    app.sequence = 1
    with urllib.request.urlopen(base + '/stream.mjpg?t=retry', timeout=3) as response:
        assert response.headers['Content-Type'].startswith('multipart/x-mixed-replace')
        assert response.read(7) == b'--frame'
    print('HTTP_OK: kiosk, original page, status, reconnect stream URL')
finally:
    server.shutdown()
    server.server_close()
