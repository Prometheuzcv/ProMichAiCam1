"""Recovery decisions, current metrics and fatal-worker process exit; no camera."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import types
import unittest
from collections import deque

ROOT = Path(__file__).resolve().parents[1]


def load_app():
    sys.modules['cv2'] = types.ModuleType('cv2')
    picamera = types.ModuleType('picamera2')
    picamera.Picamera2 = object
    sys.modules['picamera2'] = picamera
    devices = types.ModuleType('picamera2.devices')
    devices.IMX500 = object
    sys.modules['picamera2.devices'] = devices
    spec = importlib.util.spec_from_file_location('health_app', ROOT / 'app.py')
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)
    return app


class HealthTests(unittest.TestCase):
    def setUp(self):
        self.app = load_app()

    def test_startup_has_firmware_grace_then_fails(self):
        p = dict(first_frame=None, frame=None, inference=None)
        self.assertIsNone(self.app.failure_reason(299, {}, p, 0))
        self.assertIn('startup', self.app.failure_reason(301, {}, p, 0))

    def test_separate_frame_and_inference_deadlines(self):
        p = dict(first_frame=10, frame=100, inference=99)
        self.assertIsNone(self.app.failure_reason(101, {}, p, 0))
        self.assertIn('frames', self.app.failure_reason(116, {}, p, 0))
        p.update(frame=140)
        self.assertIn('inference', self.app.failure_reason(140, {}, p, 0))
        p.update(first_frame=100, inference=None)
        self.assertIsNone(self.app.failure_reason(140, {}, p, 0))
        p.update(frame=161)
        self.assertIn('First AI', self.app.failure_reason(161, {}, p, 0))

    def test_error_is_fatal_immediately(self):
        self.assertEqual(self.app.failure_reason(1, {'error': 'sensor failed'}, {}, 0), 'sensor failed')

    def test_rates_expire_and_old_ai_count_does_not_mean_alive(self):
        samples = deque([10, 10.5, 11])
        self.assertEqual(self.app.recent_rate(samples, 11), 2)
        self.assertEqual(self.app.recent_rate(samples, 20), 0)
        self.app.state['inference_frames'] = 100
        self.assertFalse(self.app.status_snapshot()['ai_ready'])

    def test_worker_exception_exits_process_for_systemd(self):
        code = '''
import sys
sys.path.insert(0, sys.argv[1])
from test_health import load_app
app = load_app()
def broken_sensor(*args):
    raise RuntimeError('simulated sensor failure')
app.IMX500 = broken_sensor
app.camera_worker()
app.supervise_camera()
'''
        result = subprocess.run([sys.executable, '-c', code, str(ROOT / 'tests')],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('Camera supervisor', result.stdout)
        self.assertIn('simulated sensor failure', result.stdout)


if __name__ == '__main__':
    unittest.main()
