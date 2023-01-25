import logging
from typing import List

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
        self.connections: List[WebSocket] = []
        self.count_message: int = 0

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_json(data)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            request = await websocket.receive_json(mode="text")
            manager.count_message += 1
            request['numbers'] = manager.count_message
            await manager.broadcast(request)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        if len(manager.connections) == 0:
            manager.count_message = 0
    except RuntimeError as error:
        logging.error(error)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
