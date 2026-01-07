import sys
import evdev
import os
from scanner_utils import list_devices, map_key_to_char

# Configuration
OUTPUT_FILE = "scanned_codes.txt"

def select_device():
    devices = list_devices()
    print("Available devices:")
    for i, dev in enumerate(devices):
        print(f"{i}: {dev.name} ({dev.path})")
    
    if not devices:
        print("No devices found. Are you sudo?")
        return None

    try:
        selection = int(input("\nSelect the scanner device number: "))
        return devices[selection]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None


def main():
    # Check for root/sudo
    if os.geteuid() != 0:
        print("Error: This script must be run as root (sudo) to grab the input device.")
        sys.exit(1)

    print("--- Barcode Scanner Isolator ---")
    device = select_device()
    
    if not device:
        sys.exit(1)

    print(f"\nDevice '{device.name}' selected.")
    print("Attempting to grab device...")
    
    try:
        # This is the magic part: grab() claims the device exclusively.
        # No other application (including the OS/Hyprland) will receive events.
        device.grab()
        print("Device grabbed successfully! Events will NOT be sent to other apps.")
        print(f"Scanning... Output will be appended to '{OUTPUT_FILE}'")
        print("Press Ctrl+C to exit.\n")
        
        current_code = []
        is_shifted = False

        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                # Value 1 is down, 0 is up, 2 is hold
                if event.value == 1: # Key down
                    key_str = evdev.ecodes.keys[event.code]
                    
                    # Handle Shift
                    if key_str in ['KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT']:
                        is_shifted = True
                        continue
                    
                    # Map to character
                    char = map_key_to_char(event, is_shifted)
                    
                    if char == '\n':
                        # End of barcode
                        final_code = "".join(current_code)
                        print(f"Captured: {final_code}")
                        
                        with open(OUTPUT_FILE, "a") as f:
                            f.write(final_code + "\n")
                        
                        current_code = [] # Reset buffer
                    elif char:
                        current_code.append(char)
                        
                elif event.value == 0: # Key up
                    key_str = evdev.ecodes.keys[event.code]
                    if key_str in ['KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT']:
                        is_shifted = False

    except IOError as e:
        print(f"Device error: {e}")
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        try:
            device.ungrab()
            print("Device ungrabbed.")
        except:
            pass

if __name__ == "__main__":
    main()
