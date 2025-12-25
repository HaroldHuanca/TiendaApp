import hid
import sys
import time

VENDOR_ID = 0x8888
PRODUCT_ID = 0x103B


def open_scanner(vid, pid):
    devices = hid.enumerate()

    # Si la API expone `Device` (mayormente en algunas distribuciones), probarla primero
    errors = []
    diagnostics = [f"hid.enumerate() encontró {len(devices)} dispositivo(s)"]
    for i, d in enumerate(devices, 1):
        vid_d = d.get('vendor_id') or 0
        pid_d = d.get('product_id') or 0
        path_d = d.get('path')
        prod = d.get('product_string')
        # decodificar path/product si vienen como bytes
        if isinstance(path_d, (bytes, bytearray)):
            try:
                path_display = path_d.decode()
            except Exception:
                path_display = repr(path_d)
        else:
            path_display = path_d
        if isinstance(prod, (bytes, bytearray)):
            try:
                prod_display = prod.decode()
            except Exception:
                prod_display = repr(prod)
        else:
            prod_display = prod
        diagnostics.append(f"{i}: vendor_id=0x{vid_d:04X} product_id=0x{pid_d:04X} path={path_display} prod={prod_display}")

    # 1) Intentar usar hid.Device (si existe)
    if hasattr(hid, 'Device'):
        try:
            return hid.Device(vid, pid)
        except Exception as e:
            errors.append(("direct", str(e)))
        # intentar abrir por path con Device
        for d in devices:
            if d.get('vendor_id') == vid and d.get('product_id') == pid:
                path = d.get('path')
                if isinstance(path, (bytes, bytearray)):
                    try:
                        path = path.decode()
                    except Exception:
                        pass
                try:
                    return hid.Device(path=path)
                except Exception as e:
                    errors.append((path, str(e)))

    # 2) Intentar usar hid.device() (API común en hidapi)
    if hasattr(hid, 'device'):
        try:
            dev = hid.device()
            # try open by vid/pid
            try:
                dev.open(vid, pid)
                return dev
            except Exception as e_open:
                errors.append((f"open({vid},{pid})", str(e_open)))
                # try open_path if available for each enumerated device
                for d in devices:
                    path = d.get('path')
                    if isinstance(path, (bytes, bytearray)):
                        try:
                            path_str = path.decode()
                        except Exception:
                            path_str = None
                    else:
                        path_str = path
                    if not path_str:
                        continue
                    try:
                        dev2 = hid.device()
                        if hasattr(dev2, 'open_path'):
                            dev2.open_path(path_str)
                        else:
                            # algunos bindings aceptan open(path) — intentar con open
                            try:
                                dev2.open(path_str)
                            except Exception:
                                raise
                        return dev2
                    except Exception as e2:
                        errors.append((path_str, str(e2)))

        except Exception as e_outer:
            errors.append(("device_block", str(e_outer)))

    # Si llegamos aquí, no se pudo abrir nada: construir mensaje diagnóstico
    msg = ["No se pudo abrir el dispositivo HID.", "Intentos directos y por path fallaron.", "--- Enumeración ---"]
    msg.extend(diagnostics)
    if errors:
        msg.append("--- Errores al intentar abrir ---")
        for p, err in errors:
            msg.append(f"{p}: {err}")
    msg.append("")
    msg.append("Posibles soluciones:")
    msg.append(" - Ejecuta el script como root (sudo) para verificar si es un problema de permisos.")
    msg.append(" - Añade una regla udev para permitir acceso a /dev/hidraw* para tu usuario.")
    msg.append(" - Verifica si el lector es un 'keyboard wedge' (emula teclado). En ese caso no aparecerá en hidapi y deberás leer desde la entrada estándar o usar evdev.")
    raise RuntimeError('\n'.join(msg))


scanner = open_scanner(VENDOR_ID, PRODUCT_ID)

print("Escaner conectado. Escanea un código...")

code_buffer = ""

try:
    while True:
        data = scanner.read(64)
        if data:
            # Procesar cada byte: si es Enter (0x0A) o Retorno (0x0D), terminar código
            for byte in data:
                if byte == 0x0A or byte == 0x0D:  # Enter o Retorno de carro
                    if code_buffer:
                        print("Código leído:", code_buffer)
                        code_buffer = ""
                elif 0x1F < byte < 0x7F:  # Caracteres ASCII imprimibles
                    code_buffer += chr(byte)
        time.sleep(0.01)
except KeyboardInterrupt:
    try:
        scanner.close()
    except Exception:
        pass
    print("Cerrando escáner.")
    sys.exit(0)
