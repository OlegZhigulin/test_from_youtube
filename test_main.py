from fastapi.testclient import TestClient
import pytest
from test_from_youtube.main import app, manager
from httpx import AsyncClient

client = TestClient(app)
async_client = AsyncClient(app=app, base_url="http://127.0.0.1:8000")

def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200

def test_websocket():
    client = TestClient(app)
    client_id = 404 
    with client.websocket_connect(f"/ws/{client_id}") as websocket:
        manager.connect(websocket, client_id)
        send_data = {"text": "Hello WebSocket"}
        websocket.send_json(send_data, mode="text")
        data = websocket.receive_json()
        assert data == {"text": "Hello WebSocket", "numbers": 1}
        send_data = {"text": "Hello WebSocket"}
        websocket.send_json(send_data, mode="text")
        data = websocket.receive_json()
        assert data == {"text": "Hello WebSocket", "numbers": 2}        
        

