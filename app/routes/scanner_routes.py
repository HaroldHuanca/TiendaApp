from flask import Blueprint, render_template, request, Response, jsonify, session, redirect, url_for
from app.services.scanner_service import ScannerService

scanner_bp = Blueprint('scanner_bp', __name__)
scanner_service = ScannerService()


@scanner_bp.route('/config', methods=['GET'])
def config_page():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('configuracion_scanner.html', usuario=session.get('usuario'))


@scanner_bp.route('/list_devices', methods=['GET'])
def list_devices():
    only_connected = request.args.get('only_connected', '0').lower() in {'1', 'true', 'yes'}
    devices = scanner_service.list_devices(only_connected=only_connected)
    return jsonify({
        'devices': devices,
        'status': scanner_service.get_status()
    })


@scanner_bp.route('/connect', methods=['POST'])
def connect():
    data = request.get_json(silent=True) or {}
    device_identifier = data.get('device_id') or data.get('path')
    if not device_identifier:
        return jsonify({'success': False, 'message': 'Se requiere el identificador del dispositivo'})

    success = scanner_service.connect_device(device_identifier)
    return jsonify({'success': success, 'status': scanner_service.get_status()})


@scanner_bp.route('/disconnect', methods=['POST'])
def disconnect():
    data = request.get_json(silent=True) or {}
    device_identifier = data.get('device_id') or data.get('path')
    scanner_service.disconnect_device(device_identifier)
    return jsonify({'success': True, 'status': scanner_service.get_status()})


@scanner_bp.route('/status', methods=['GET'])
def status():
    return jsonify(scanner_service.get_status())


@scanner_bp.route('/stream')
def stream():
    selected_device_id = request.args.get('device_id') or None

    def event_stream():
        q = scanner_service.listen(selected_device_id)
        try:
            while True:
                try:
                    data = q.get(timeout=15)
                    yield f"data: {data}\n\n"
                except Exception:
                    yield ": heartbeat\n\n"
        except GeneratorExit:
            scanner_service.queues.pop(q, None)

    return Response(event_stream(), mimetype="text/event-stream")
