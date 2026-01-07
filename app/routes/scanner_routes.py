from flask import Blueprint, render_template, request, Response, jsonify, session, redirect, url_for
from app.services.scanner_service import ScannerService
import json
import time

scanner_bp = Blueprint('scanner_bp', __name__)
scanner_service = ScannerService()

@scanner_bp.route('/config', methods=['GET'])
def config_page():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('configuracion_scanner.html', usuario=session.get('usuario'))

@scanner_bp.route('/list_devices', methods=['GET'])
def list_devices():
    devices = scanner_service.list_devices()
    return jsonify({
        'devices': devices,
        'status': scanner_service.get_status()
    })

@scanner_bp.route('/connect', methods=['POST'])
def connect():
    data = request.json
    device_path = data.get('path')
    if not device_path:
        return jsonify({'success': False, 'message': 'Path required'})
    
    success = scanner_service.connect_device(device_path)
    return jsonify({'success': success})

@scanner_bp.route('/disconnect', methods=['POST'])
def disconnect():
    scanner_service.disconnect_device()
    return jsonify({'success': True})

@scanner_bp.route('/status', methods=['GET'])
def status():
    return jsonify(scanner_service.get_status())

@scanner_bp.route('/stream')
def stream():
    def event_stream():
        q = scanner_service.listen()
        try:
            while True:
                # Blok here waiting for next scan or heartbeat
                # We need a timeout to send heartbeats or detect disconnects
                try:
                    # Wait for 15 seconds max
                    data = q.get(timeout=15)
                    yield f"data: {data}\n\n"
                except:
                    # Timeout, send heartbeat
                    yield f": heartbeat\n\n"
        except GeneratorExit:
            scanner_service.queues.remove(q)

    return Response(event_stream(), mimetype="text/event-stream")
