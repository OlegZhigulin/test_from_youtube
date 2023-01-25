from fastapi.testclient import TestClient
import pytest
from test_from_youtube.main import app, manager
from httpx import AsyncClient
client = TestClient(app)


def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_websocket():
    client = TestClient(app)
    client_id = 404 
    with client.websocket_connect(f"/ws/{client_id}") as websocket:
        manager.connect(websocket)
        send_data = {"text": "Hello WebSocket"}
        websocket.send_json(send_data, mode="text")
        data = websocket.receive_json()
        assert data == {"text": "Hello WebSocket", "numbers": 1}

def test_websocket_next_user():
    client = TestClient(app)
    client_id = 500 
    with client.websocket_connect(f"/ws/{client_id}") as websocket:
        manager.connect(websocket)
        send_data = {"text": "Hello WebSocket"}
        websocket.send_json(send_data, mode="text")
        data = websocket.receive_json()
        assert data == {"text": "Hello WebSocket", "numbers": 2}