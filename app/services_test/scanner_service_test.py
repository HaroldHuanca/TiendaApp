import json
import unittest
from unittest.mock import Mock, patch, mock_open

from app.services import scanner_service


class TestScannerService(unittest.TestCase):
    def setUp(self):
        scanner_service.ScannerService._instance = None
        self.service = scanner_service.ScannerService()

    @patch('app.services.scanner_service.play_error_sound')
    @patch('app.services.scanner_service.speak_text')
    @patch('app.services.scanner_service.venta_individual_service.insertar_venta_individual')
    @patch('app.services.scanner_service.producto_service.obtener_producto_por_id')
    @patch('app.services.scanner_service.producto_service.buscar_id_por_codigo_barras')
    def test_process_scanned_code_registers_sale(self, mock_lookup, mock_get_product, mock_insert, mock_speak, mock_error_sound):
        mock_lookup.return_value = 7
        mock_get_product.return_value = {
            'id': 7,
            'descripcion': 'Café',
            'precio_venta': 12.5,
            'stock': 3.0
        }

        result = self.service.process_scanned_code('1234567890123')

        self.assertTrue(result['success'])
        self.assertEqual(result['product']['descripcion'], 'Café')
        mock_insert.assert_called_once()
        mock_speak.assert_called_once()
        mock_error_sound.assert_not_called()

    @patch.object(scanner_service.ScannerService, 'process_scanned_code')
    def test_broadcast_skips_duplicate_scan(self, mock_process):
        self.service._broadcast('1234567890123', 'scanner-1')
        self.service._broadcast('1234567890123', 'scanner-1')

        mock_process.assert_called_once_with('1234567890123', device_id='scanner-1')

    @patch('app.services.scanner_service.evdev.InputDevice')
    @patch.object(scanner_service.ScannerService, '_discover_devices', return_value=[{
        'id': 'scanner-1',
        'name': 'Lector 1',
        'path': '/dev/input/event0'
    }])
    def test_connect_device_by_identifier(self, mock_discover, mock_input_device):
        mock_device = Mock()
        mock_device.grab.return_value = None
        mock_device.ungrab.return_value = None
        mock_device.read_loop.return_value = iter([])
        mock_input_device.return_value = mock_device

        success = self.service.connect_device('scanner-1', save=False)

        self.assertTrue(success)
        self.assertEqual(self.service.active_device_id, 'scanner-1')
        self.assertEqual(self.service.current_device_path, '/dev/input/event0')
        self.assertIn('scanner-1', self.service.connected_devices)
        mock_input_device.assert_called_once_with('/dev/input/event0')

    @patch.object(scanner_service.ScannerService, 'connect_device')
    def test_load_config_auto_connects_all_saved_devices(self, mock_connect):
        config_payload = {
            'selected_device_id': 'scanner-1',
            'devices': {
                'scanner-1': {'id': 'scanner-1', 'path': '/dev/input/event0', 'name': 'Lector 1', 'connected': True},
                'scanner-2': {'id': 'scanner-2', 'path': '/dev/input/event1', 'name': 'Lector 2', 'connected': True}
            }
        }

        with patch('app.services.scanner_service.os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(config_payload))):
            scanner_service.ScannerService._instance = None
            scanner_service.ScannerService()

        self.assertEqual(mock_connect.call_count, 2)
        mock_connect.assert_any_call('/dev/input/event0', save=False)
        mock_connect.assert_any_call('/dev/input/event1', save=False)

    @patch('app.services.scanner_service.evdev.InputDevice')
    @patch.object(scanner_service.ScannerService, '_discover_devices', return_value=[{
        'id': 'scanner-1',
        'name': 'Lector 1',
        'path': '/dev/input/event0'
    }])
    def test_disconnect_device_closes_input_device(self, mock_discover, mock_input_device):
        mock_device = Mock()
        mock_device.grab.return_value = None
        mock_device.ungrab.return_value = None
        mock_device.close.return_value = None
        mock_device.read_loop.return_value = iter([])
        mock_input_device.return_value = mock_device

        success = self.service.connect_device('scanner-1', save=False)
        self.assertTrue(success)

        disconnected = self.service.disconnect_device('scanner-1')

        self.assertTrue(disconnected)
        self.assertNotIn('scanner-1', self.service.connected_devices)
        mock_device.ungrab.assert_called_once()
        mock_device.close.assert_called_once()

    @patch('app.services.scanner_service.evdev.InputDevice')
    @patch.object(scanner_service.ScannerService, '_discover_devices', return_value=[{
        'id': 'scanner-1',
        'name': 'Lector 1',
        'path': '/dev/input/event0'
    }])
    def test_disconnect_device_by_path_closes_input_device(self, mock_discover, mock_input_device):
        mock_device = Mock()
        mock_device.grab.return_value = None
        mock_device.ungrab.return_value = None
        mock_device.close.return_value = None
        mock_device.read_loop.return_value = iter([])
        mock_input_device.return_value = mock_device

        success = self.service.connect_device('scanner-1', save=False)
        self.assertTrue(success)

        disconnected = self.service.disconnect_device('/dev/input/event0')

        self.assertTrue(disconnected)
        self.assertNotIn('scanner-1', self.service.connected_devices)
        mock_device.ungrab.assert_called_once()
        mock_device.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
