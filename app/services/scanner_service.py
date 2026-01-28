import evdev
import threading
import queue
import time
import json
import os

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

class ScannerService:
    _instance = None
    CONFIG_FILE = 'scanner_config.json'
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScannerService, cls).__new__(cls)
            cls._instance.device = None
            cls._instance.stop_event = threading.Event()
            cls._instance.thread = None
            cls._instance.queues = set()
            cls._instance.current_device_path = None
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Attempt to load saved configuration and auto-connect"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    path = config.get('device_path')
                    if path and os.path.exists(path):
                        print(f"Auto-connecting to saved scanner: {path}")
                        self.connect_device(path, save=False)
            except Exception as e:
                print(f"Error loading scanner config: {e}")

    def _save_config(self, path):
         try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump({'device_path': path}, f)
         except Exception as e:
             print(f"Error saving scanner config: {e}")

    def list_devices(self):
        try:
            return [{'name': dev.name, 'path': dev.path} for dev in [evdev.InputDevice(path) for path in evdev.list_devices()]]
        except Exception as e:
            print(f"Error listing devices: {e}")
            return []

    def connect_device(self, device_path, save=True):
        self.disconnect_device()
        
        try:
            self.device = evdev.InputDevice(device_path)
            self.device.grab() # Exclusive access
            self.current_device_path = device_path
            
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._read_loop, daemon=True)
            self.thread.start()
            print(f"Connected to scanner: {self.device.name}")
            
            if save:
                self._save_config(device_path)
                
            return True
        except Exception as e:
            print(f"Failed to connect to scanner: {e}")
            return False

    def disconnect_device(self):
        if self.device:
            self.stop_event.set()
            # Try to force ungrab safely
            try:
                self.device.ungrab()
            except:
                pass
            self.device = None
            self.current_device_path = None
            
            # Remove config file on explicit disconnect
            if os.path.exists(self.CONFIG_FILE):
                try:
                    os.remove(self.CONFIG_FILE)
                except:
                    pass
            
            print("Scanner disconnected")

    def _read_loop(self):
        current_code = []
        is_shifted = False
        
        print("Starting scanner loop")
        try:
            # We use a non-blocking loop or select, but evdev's read_loop is usually blocking.
            # to make it stoppable, we can't easily break a blocking read without an event.
            # However, for simplicity, since we are in a daemon thread, it will die with the app.
            # But reconnecting requires stopping this loop. 
            # Ideally we use select to timeout.
            
            for event in self.device.read_loop():
                if self.stop_event.is_set():
                    break
                
                if event.type == evdev.ecodes.EV_KEY:
                    if event.value == 1: # Key down
                        key_str = evdev.ecodes.keys[event.code]
                        
                        if key_str in ['KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT']:
                            is_shifted = True
                            continue
                        
                        char = map_key_to_char(event, is_shifted)
                        
                        if char == '\n':
                            final_code = "".join(current_code)
                            self._broadcast(final_code)
                            current_code = []
                        elif char:
                            current_code.append(char)
                            
                    elif event.value == 0: # Key up
                        key_str = evdev.ecodes.keys[event.code]
                        if key_str in ['KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT']:
                            is_shifted = False
        except Exception as e:
            print(f"Error in scanner loop: {e}")
            self.disconnect_device()

    def _broadcast(self, code):
        print(f"Broadcasting scan: {code}")
        # Clean up dead queues
        dead_queues = set()
        for q in self.queues:
            try:
                q.put(code)
            except:
                dead_queues.add(q)
        
        for q in dead_queues:
            self.queues.remove(q)

    def listen(self):
        q = queue.Queue()
        self.queues.add(q)
        return q

    def get_status(self):
        return {
            'connected': self.device is not None,
            'device_name': self.device.name if self.device else None,
            'device_path': self.current_device_path
        }
