import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict, List, Callable

from jq_func import long_task

executor = ThreadPoolExecutor(max_workers=1)
tasks: Dict[str, Future] = {}


def run_long_task(task_id: str, data: dict,
                  notify_callback: Callable[[str, str], None]):
    print(f'run {task_id}')
    result = asyncio.run(long_task(data))
    #result = long_task(data)
    asyncio.run(notify_callback(task_id, result))


def submit_task(data: str, notify_callback: Callable[[str, str], None]) -> str:
    task_id = str(uuid.uuid4())
    future = executor.submit(run_long_task, task_id, data, notify_callback)
    tasks[task_id] = future
    return task_id


def get_task_status(task_id: str):
    task = tasks.get(task_id)
    if task is None:
        return {"status": "not found"}
    elif task.done():
        return {"status": "fin", "result": task.result()}
    else:
        return {"status": "processing"}


def list_all_tasks() -> List[Dict[str, str]]:
    all_tasks = []
    for task_id, future in tasks.items():
        status = "fin" if future.done() else "processing"
        result = future.result() if future.done() else None
        all_tasks.append({
            "task_id": task_id,
            "status": status,
            "result": result
        })

    completed_tasks = [
        task_id for task_id, future in tasks.items() if future.done()
    ]
    for task_id in completed_tasks:
        del tasks[task_id]

    return all_tasks
