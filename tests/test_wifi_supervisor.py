"""Policy tests without disconnecting the physical Raspberry Pi."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('wifi_supervisor',
    Path(__file__).resolve().parents[1] / 'deploy' / 'wifi-supervisor.py')
wifi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wifi)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.profiles = [{'uuid': 'one', 'ssid': 'home', 'bssid': 'AA'},
                         {'uuid': 'two', 'ssid': 'other', 'bssid': ''}]
        self.aps = [{'IN-USE': '*', 'SSID': 'home', 'BSSID': 'AA', 'SIGNAL': 40},
                    {'IN-USE': '', 'SSID': 'other', 'BSSID': 'BB', 'SIGNAL': 80}]

    def test_offline_alternates_forever(self):
        state = {}
        self.assertEqual([wifi.plan(self.profiles, state, t, 30, '')
                          for t in range(8)], ['one', 'two'] * 4)

    def test_does_not_interrupt_activation_or_unavailable_radio(self):
        for status in (10, 20, 40, 50, 60, 70, 80, 90, 110):
            self.assertIsNone(wifi.plan(self.profiles, {}, 1000, status, ''))

    def test_requires_two_good_scans_and_sets_fallback(self):
        state = {}
        self.assertIsNone(wifi.plan(self.profiles, state, 1000, 100, 'one', self.aps))
        self.assertEqual(wifi.plan(self.profiles, state, 1300, 100, 'one', self.aps), 'two')
        self.assertEqual(wifi.plan(self.profiles, state, 1400, 30, ''), 'one')

    def test_weak_or_small_improvement_does_not_switch(self):
        for current, candidate in ((50, 59), (65, 80), (80, 75)):
            self.aps[0]['SIGNAL'], self.aps[1]['SIGNAL'] = current, candidate
            state = {}
            for now in (1000, 1300, 1600):
                self.assertIsNone(wifi.plan(self.profiles, state, now, 100, 'one', self.aps))

    def test_bad_scan_breaks_confirmation_sequence(self):
        state = {}
        wifi.plan(self.profiles, state, 1000, 100, 'one', self.aps)
        wifi.plan(self.profiles, state, 1300, 100, 'one', self.aps[:1])
        self.assertIsNone(wifi.plan(self.profiles, state, 1600, 100, 'one', self.aps))

    def test_cooldown_and_other_connections_are_respected(self):
        state = {'last_switch': 900}
        for now in (1000, 1300):
            self.assertIsNone(wifi.plan(self.profiles, state, now, 100, 'one', self.aps))
        self.assertIsNone(wifi.plan(self.profiles, {}, 2000, 100, 'unknown', self.aps))

    def test_bssid_pin_filters_other_points_of_same_ssid(self):
        self.profiles[1]['bssid'] = 'CC'
        state = {}
        for now in (1000, 1300):
            self.assertIsNone(wifi.plan(self.profiles, state, now, 100, 'one', self.aps))

    def test_multiline_parser_keeps_colons_in_ssid_and_bssid(self):
        rows = wifi.parse_access_points('IN-USE: *\nSSID: a:b\nBSSID: AA:BB:CC:DD:EE:FF\nSIGNAL: 72\n')
        self.assertEqual(rows[0]['SSID'], 'a:b')
        self.assertEqual(rows[0]['BSSID'], 'AA:BB:CC:DD:EE:FF')
        self.assertEqual(rows[0]['SIGNAL'], 72)


if __name__ == '__main__':
    unittest.main()
