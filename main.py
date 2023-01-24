import logging

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

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            request = await websocket.receive_json(mode="text")
            await websocket.send_json(request)
        except WebSocketDisconnect as error:
            logging.error(error)
            break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
