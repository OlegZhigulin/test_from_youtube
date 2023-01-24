from fastapi.testclient import TestClient

from test_from_youtube.main import app

client = TestClient(app)


def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        send_data = {"text": "Hello World"}
        websocket.send_json(send_data, mode="text")
        data = websocket.receive_json(mode="text")
        assert data == send_data
