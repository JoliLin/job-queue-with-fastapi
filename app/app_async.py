import pathlib
import sys

cur = pathlib.Path(__file__).resolve().parent
sys.path.append('{}/'.format(cur.parent))
sys.path.append('{}/jq'.format(cur.parent))

import uvicorn

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Form
from typing import Dict

from jq import submit_task, get_task_status, list_all_tasks


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, task_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[task_id] = websocket

    def disconnect(self, task_id: str):
        self.active_connections.pop(task_id, None)

    async def send_message(self, task_id: str, message: str):
        websocket = self.active_connections.get(task_id)
        if websocket:
            await websocket.send_text(message)


manager = ConnectionManager()

router = APIRouter(
    prefix="/api-async",
    tags=["async"],
)


@router.post("/submit-task/")
async def submit_task_endpoint(data: str = Form(...)):
    print(data)

    async def notify_task_completion(task_id: str, result: str):
        await manager.send_message(task_id, result)

    data = {'uid': data}
    task_id = submit_task(data, notify_task_completion)
    return {"task_id": task_id}


@router.get("/task-status/{task_id}")
async def get_task_status_endpoint(task_id: str):
    status = get_task_status(task_id)
    return status


@router.post("/list-all-tasks/")
async def list_all():
    tasks = list_all_tasks()
    return {"tasks": tasks}


@router.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await manager.connect(task_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(task_id)
