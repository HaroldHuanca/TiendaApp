import evdev

# Standard QWERTY mapping for US layout (common for scanners)
# Maps evdev key codes (e.g., 'KEY_A') to characters
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

def list_devices():
    """Returns a list of available input devices."""
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    return devices

def map_key_to_char(key_event, is_shifted=False):
    """
    Maps a key event to a character.
    Returns None if the key is not mapped (e.g. modifier keys themselves).
    """
    key_code = evdev.ecodes.keys[key_event.code]
    
    if isinstance(key_code, list):
         # Sometimes multiple keys map to same scancode or vice versa, key_code might be list
         # usually evdev.ecodes.keys[code] returns a string like 'KEY_A'
         key_code = key_code[0]

    char = SCANCODE_MAP.get(key_code)
    
    if char and is_shifted:
        return SHIFT_MAP.get(char, char)
    
    return char
