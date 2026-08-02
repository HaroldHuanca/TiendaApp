import atexit
import signal
import evdev
import threading
import queue
import json
import os
import time
from datetime import datetime

import app.services.producto_service as producto_service
import app.services.venta_individual_service as venta_individual_service
import app.services.tiempo_service as tiempo_service

producto_model = producto_service.producto_model

# Reusing mapping logic from scanner_utils to avoid duplication issues
# Ideally we would move scanner_utils to app/utils/ but inlining is safer for now to avoid path issues
SCANCODE_MAP = {
    'KEY_0': '0', 'KEY_1': '1', 'KEY_2': '2', 'KEY_3': '3', 'KEY_4': '4',
    'KEY_5': '5', 'KEY_6': '6', 'KEY_7': '7', 'KEY_8': '8', 'KEY_9': '9',
    'KEY_A': 'a', 'KEY_B': 'b', 'KEY_C': 'c', 'KEY_D': 'd', 'KEY_E': 'e',
    'KEY_F': 'f', 'KEY_G': 'g', 'KEY_H': 'h', 'KEY_I': 'i', 'KEY_J': 'j',
    'KEY_K': 'k', 'KEY_L': 'l', 'KEY_M': 'm', 'KEY_N': 'n', 'KEY_O': 'o',
    'KEY_P': 'p', 'KEY_Q': 'q', 'KEY_R': 'r', 'KEY_S': 's', 'KEY_T': 't',
    'KEY_U': 'u', 'KEY_V': 'v', 'KEY_W': 'w', 'KEY_X': 'x', 'KEY_Y': 'y',
    'KEY_Z': 'z',
    'KEY_MINUS': '-', 'KEY_EQUAL': '=', 'KEY_LEFTBRACE': '[', 'KEY_RIGHTBRACE': ']',
    'KEY_BACKSLASH': '\\', 'KEY_SEMICOLON': ';', 'KEY_APOSTROPHE': "'",
    'KEY_GRAVE': '`', 'KEY_COMMA': ',', 'KEY_DOT': '.', 'KEY_SLASH': '/',
    'KEY_SPACE': ' ',
    'KEY_ENTER': '\n', 'KEY_KpEnter': '\n'
}

SHIFT_MAP = {
    '0': ')', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(',
    '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"', '`': '~', ',': '<', '.': '>', '/': '?',
    'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J',
    'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T',
    'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z'
}


def map_key_to_char(key_event, is_shifted=False):
    key_code = evdev.ecodes.keys[key_event.code]
    if isinstance(key_code, list):
        key_code = key_code[0]
    char = SCANCODE_MAP.get(key_code)
    if char and is_shifted:
        return SHIFT_MAP.get(char, char)
    return char


def play_error_sound():
    return None


def speak_text(text):
    return text


class ScannerService:
    _instance = None
    CONFIG_FILE = 'scanner_config.json'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScannerService, cls).__new__(cls)
            cls._instance.connected_devices = {}
            cls._instance.device_stop_events = {}
            cls._instance.queues = {}
            cls._instance.active_device_id = None
            cls._instance.current_device_path = None
            cls._instance._last_broadcast = {}
            cls._instance._last_processed_scans = {}
            cls._instance._persisted_devices = {}
            cls._instance._shutdown_registered = False
            cls._instance._register_shutdown()
            cls._instance._load_config()
        return cls._instance

    def _register_shutdown(self):
        if not getattr(self, '_shutdown_registered', False):
            atexit.register(self.shutdown_all_devices)
            try:
                signal.signal(signal.SIGINT, self._signal_handler)
                signal.signal(signal.SIGTERM, self._signal_handler)
            except Exception:
                pass
            self._shutdown_registered = True

    def _signal_handler(self, signum, frame):
        print(f"Received shutdown signal: {signum}")
        self.shutdown_all_devices()

    def shutdown_all_devices(self):
        try:
            for device_id in list(self.connected_devices.keys()):
                self.disconnect_device(device_id, persist=False)
        except Exception as e:
            print(f"Error during scanner shutdown: {e}")

    def _load_config(self):
        """Carga la configuración persistida y auto-conecta solo los dispositivos marcados para reconexión."""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.active_device_id = config.get('selected_device_id')
                    saved_devices = config.get('devices') or {}
                    self._persisted_devices = dict(saved_devices)
                    reconnect_ids = []
                    for device_id, metadata in saved_devices.items():
                        if metadata and metadata.get('connected', False):
                            reconnect_ids.append(device_id)

                    if reconnect_ids:
                        print(f"Auto-connecting saved scanners: {reconnect_ids}")
                        for device_id, metadata in saved_devices.items():
                            if metadata and metadata.get('connected', False):
                                identifier = metadata.get('path') or metadata.get('id') or device_id
                                self.connect_device(identifier, save=False)
            except Exception as e:
                print(f"Error loading scanner config: {e}")

    def _save_config(self):
        try:
            payload = {
                'selected_device_id': self.active_device_id,
                'devices': {}
            }

            for device_id, metadata in self._persisted_devices.items():
                payload['devices'][device_id] = dict(metadata)

            for device_id, state in self.connected_devices.items():
                payload['devices'][device_id] = {
                    'id': device_id,
                    'path': state.get('path'),
                    'name': state.get('name'),
                    'connected': True
                }
                self._persisted_devices[device_id] = payload['devices'][device_id]

            for device_id, metadata in list(payload['devices'].items()):
                if metadata.get('path'):
                    payload['devices'][metadata['path']] = dict(metadata)
                    payload['devices'][metadata['path']]['connected'] = metadata.get('connected', False)

            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(payload, f)
        except Exception as e:
            print(f"Error saving scanner config: {e}")

    def _discover_devices(self):
        try:
            devices = []
            for path in evdev.list_devices():
                try:
                    device = evdev.InputDevice(path)
                    devices.append(self._build_device_info(device))
                except Exception:
                    continue
            return devices
        except Exception as e:
            print(f"Error listing devices: {e}")
            return []

    def _build_device_info(self, device):
        info = getattr(device, 'info', None)
        vendor = getattr(info, 'vendor', None)
        product = getattr(info, 'product', None)
        version = getattr(info, 'version', None)
        phys = getattr(device, 'phys', None) or ''
        uniq = getattr(device, 'uniq', None) or ''
        name = getattr(device, 'name', None) or 'Dispositivo desconocido'
        path = getattr(device, 'path', None) or ''

        raw_parts = [str(value) for value in [vendor, product, version, phys, uniq, name] if value]
        device_id = ':'.join(raw_parts) or path or name
        inferred_type = self._infer_device_type(name, path, vendor, product, phys, uniq)
        return {
            'id': device_id,
            'name': name,
            'path': path,
            'vendor': vendor,
            'product': product,
            'version': version,
            'phys': phys,
            'uniq': uniq,
            'type': inferred_type
        }

    def _infer_device_type(self, name, path, vendor, product, phys, uniq):
        haystack = ' '.join(filter(None, [str(name), str(path), str(vendor), str(product), str(phys), str(uniq)])).lower()
        keywords = ['hid', 'scanner', 'barcode', 'usb', 'input', 'keyboard', 'reader']
        if any(keyword in haystack for keyword in keywords):
            return 'scanner'
        return 'other'

    def _resolve_device(self, identifier):
        if not identifier:
            return None

        for device in self._discover_devices():
            if device['id'] == identifier or device['path'] == identifier:
                return device
        return None

    def list_devices(self, only_connected=False):
        available_devices = self._discover_devices()
        compatible_devices = [device for device in available_devices if device.get('type') == 'scanner']
        connected_ids = set(self.connected_devices.keys())
        filtered_devices = []
        for device in compatible_devices:
            if only_connected and device['id'] not in connected_ids:
                continue
            device['connected'] = device['id'] in connected_ids
            device['selected'] = device['id'] == self.active_device_id
            filtered_devices.append(device)
        return filtered_devices

    def connect_device(self, identifier, save=True):
        device_info = self._resolve_device(identifier)
        if not device_info:
            return False

        device_id = device_info['id']
        if device_id in self.connected_devices:
            self.active_device_id = device_id
            self.current_device_path = device_info['path']
            if save:
                self._save_config()
            return True

        try:
            device = evdev.InputDevice(device_info['path'])
            device.grab()
            self.connected_devices[device_id] = {
                'device': device,
                'path': device_info['path'],
                'name': device_info['name']
            }
            self.device_stop_events[device_id] = threading.Event()
            self.active_device_id = device_id
            self.current_device_path = device_info['path']
            self._persisted_devices[device_id] = {
                'id': device_id,
                'path': device_info['path'],
                'name': device_info['name'],
                'connected': True
            }

            thread = threading.Thread(target=self._read_loop, args=(device_id,), daemon=True)
            thread.start()
            self.connected_devices[device_id]['thread'] = thread
            print(f"Connected to scanner: {device_info['name']}")

            if save:
                self._save_config()
            return True
        except OSError as e:
            if getattr(e, 'errno', None) == 16:
                print(f"Scanner device busy on connect: {device_info['path']}")
                try:
                    self.disconnect_device(device_id, persist=False)
                except Exception:
                    pass
            print(f"Failed to connect to scanner: {e}")
            return False
        except Exception as e:
            print(f"Failed to connect to scanner: {e}")
            return False

    def disconnect_device(self, identifier=None, persist=True):
        disconnect_ids = []
        if identifier:
            if identifier in self.connected_devices:
                disconnect_ids = [identifier]
            else:
                for device_id, state in self.connected_devices.items():
                    if state.get('path') == identifier:
                        disconnect_ids.append(device_id)
        else:
            disconnect_ids = list(self.connected_devices.keys())

        for device_id in disconnect_ids:
            state = self.connected_devices.pop(device_id, None)
            if not state:
                continue

            stop_event = self.device_stop_events.pop(device_id, None)
            if stop_event:
                stop_event.set()

            device = state.get('device')
            if device:
                try:
                    device.ungrab()
                except Exception:
                    pass
                try:
                    device.close()
                except Exception:
                    pass

            if self.active_device_id == device_id:
                self.active_device_id = None
            if self.current_device_path == state.get('path'):
                self.current_device_path = None

            persistence_metadata = {
                'id': device_id,
                'path': state.get('path'),
                'name': state.get('name'),
                'connected': False if persist else True
            }
            self._persisted_devices[device_id] = persistence_metadata
            if state.get('path'):
                self._persisted_devices[state.get('path')] = dict(persistence_metadata)

        if not self.connected_devices:
            self.active_device_id = None
            self.current_device_path = None

        if persist:
            self._save_config()
        print("Scanner disconnected")
        return True

    def set_active_device(self, identifier):
        device_info = self._resolve_device(identifier)
        if not device_info:
            return False
        self.active_device_id = device_info['id']
        self.current_device_path = device_info['path']
        self._save_config()
        return True

    def _read_loop(self, device_id):
        current_code = []
        is_shifted = False
        state = self.connected_devices.get(device_id)
        if not state:
            return

        device = state['device']
        stop_event = self.device_stop_events.get(device_id)
        print("Starting scanner loop")
        try:
            for event in device.read_loop():
                if stop_event and stop_event.is_set():
                    break

                if event.type == evdev.ecodes.EV_KEY:
                    if event.value == 1:
                        key_str = evdev.ecodes.keys[event.code]

                        if key_str in ['KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT']:
                            is_shifted = True
                            continue

                        char = map_key_to_char(event, is_shifted)

                        if char == '\n':
                            final_code = ''.join(current_code).strip()
                            if final_code:
                                self._broadcast(final_code, device_id)
                            current_code = []
                        elif char:
                            current_code.append(char)

                    elif event.value == 0:
                        key_str = evdev.ecodes.keys[event.code]
                        if key_str in ['KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT']:
                            is_shifted = False
        except Exception as e:
            print(f"Error in scanner loop: {e}")
            self.disconnect_device(device_id)

    def _broadcast(self, code, device_id):
        now = time.monotonic()
        last_scan = self._last_broadcast.get(device_id)
        if last_scan and last_scan.get('code') == code and (now - last_scan.get('time', 0)) < 1.5:
            print(f"Skipping duplicate scan from {device_id}: {code}")
            return

        self._last_broadcast[device_id] = {'code': code, 'time': now}

        print(f"Broadcasting scan from {device_id}: {code}")
        dead_queues = set()

        for q, selected_device_id in list(self.queues.items()):
            if selected_device_id and selected_device_id != device_id:
                continue
            try:
                q.put(code)
            except Exception:
                dead_queues.add(q)

        for q in dead_queues:
            self.queues.pop(q, None)

        self.process_scanned_code(code, device_id=device_id)

    def listen(self, selected_device_id=None):
        q = queue.Queue()
        self.queues[q] = selected_device_id
        return q

    def get_status(self):
        active_state = self.connected_devices.get(self.active_device_id) if self.active_device_id else None
        return {
            'connected': bool(self.connected_devices),
            'device_name': active_state.get('name') if active_state else None,
            'device_path': active_state.get('path') if active_state else None,
            'active_device_id': self.active_device_id,
            'active_device_name': active_state.get('name') if active_state else None,
            'connected_devices': [
                {'id': device_id, 'name': state.get('name'), 'path': state.get('path')}
                for device_id, state in self.connected_devices.items()
            ]
        }

    def process_scanned_code(self, code, device_id=None):
        code = str(code or '').strip()
        if not code:
            return {'success': False, 'message': 'Código vacío'}

        now = time.monotonic()
        dedupe_key = f"{device_id or 'default'}:{code}"
        last_seen = self._last_processed_scans.get(dedupe_key)
        if last_seen and (now - last_seen) < 1.5:
            print(f"Skipping already processed scan: {code}")
            return {'success': False, 'message': 'Escaneo duplicado'}
        self._last_processed_scans[dedupe_key] = now

        try:
            id_producto = producto_service.buscar_id_por_codigo_barras(code)
            if not id_producto:
                return {'success': False, 'message': 'Producto no encontrado'}

            producto = producto_service.obtener_producto_por_id(id_producto)
            if not producto:
                return {'success': False, 'message': 'Producto no encontrado'}

            fecha_hora = tiempo_service.obtener_fecha_actual_formateada_YYYYmmddHHMMSS()
            print(fecha_hora)
            venta_individual_service.insertar_venta_individual(
                id_producto,
                1,
                1.0,
                float(producto.get('precio_venta', 0)),
                fecha_hora
            )
            speak_text(f"Producto {producto.get('descripcion', code)} agregado")
            return {'success': True, 'product': producto}
        except Exception as e:
            play_error_sound()
            return {'success': False, 'message': str(e)}
