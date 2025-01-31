from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import json

app = FastAPI()

class InterviewQuestion(BaseModel):
    transcript: str
    context: list[dict]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        question = InterviewQuestion(**json.loads(data))
        # TODO: Add processing logic
        await websocket.send_text(json.dumps({"response": "Sample response"}))
