import asyncio
import uuid
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict, List, Callable


class Queuer:

    def __init__(self, long_task, max_workers=1):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: Dict[str, Future] = {}
        self.long_task = long_task

    def run_web_task(
        self, task_id: str, data: dict, notify_callback: Callable[[str, str], None]
    ):
        print(f"run {task_id}")
        result = asyncio.run(self.long_task(data))
        asyncio.run(notify_callback(task_id, result))
        return result

    def submit_web_task(
        self, data: str, notify_callback: Callable[[str, str], None]
    ) -> str:
        task_id = str(uuid.uuid4())
        future = self.executor.submit(
            self.run_web_task, task_id, data, notify_callback
        )
        self.tasks[task_id] = future
        return task_id

    def run(self, task_id: str, data: dict):
        print(f"run {task_id}")
        result = asyncio.run(self.long_task(data))
        return result

    def submit(self, data: str, task_id: str = None) -> str:
        task_id = str(uuid.uuid4()) if task_id == None else task_id
        future = self.executor.submit(self.run, task_id, data)
        self.tasks[task_id] = future
        return task_id

    def get_task_status(self, task_id: str):
        task = self.tasks.get(task_id)
        if task is None:
            return {"status": "not found"}
        elif task.done():
            return {"status": "fin", "result": task.result()}
        else:
            return {"status": "processing"}

    def check_finish(self) -> int:
        finTask = 0
        for task_id, future in self.tasks.items():
            if future.done():
                finTask += 1
        return finTask

    def get_result_util_finish(self, size_of_loop):
        while True:
            if self.check_finish() == size_of_loop:
                break
        return self.list_all_tasks()

    def list_all_tasks(self) -> List[Dict[str, str]]:
        all_tasks = []
        for task_id, future in self.tasks.items():
            status = "fin" if future.done() else "processing"
            result = future.result() if future.done() else None
            all_tasks.append({"task_id": task_id, "status": status, "result": result})

        completed_tasks = [
            task_id for task_id, future in self.tasks.items() if future.done()
        ]
        for task_id in completed_tasks:
            del self.tasks[task_id]

        return all_tasks
