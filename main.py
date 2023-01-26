import logging
from typing import Dict

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)


class ConnectionManager:
    def __init__(self):
        self.count_people_and_message: Dict[str, int] = dict()

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.count_people_and_message[client_id] = 0

    def disconnect(self, client_id: int):
        del self.count_people_and_message[client_id]


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            request = await websocket.receive_json(mode="text")
            manager.count_people_and_message[client_id] += 1
            request['numbers'] = manager.count_people_and_message[client_id]
            await websocket.send_json(request)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except RuntimeError as error:
        logging.error(error)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
