import pytest
import json
from flask import Flask
from venta_routes import venta_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(venta_bp, url_prefix="/ventas")
    return app

@pytest.fixture
def client(app):
    return app.test_client()


def test_insertar_venta(client, mocker):
    mocker.patch("app.services.venta_service.insertar_venta", return_value=10)

    venta = {
        "id_serie": 1,
        "id_usuario": 1,
        "id_cliente": 1,
        "descripcion_estado": "BOLETA",
        "fecha": "2025-08-24T15:00:00",
        "total": 150.50
    }

    response = client.post("/ventas/insertar_venta", json=venta)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["mensaje"] == "Venta registrada exitosamente"
    assert data["id"] == 10
