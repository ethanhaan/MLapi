from fastapi import FastAPI, BackgroundTasks
import uuid

def generate_unique_id():
    return str(uuid.uuid4())

def run_process(background_tasks, tasks, function, args):
    task_id = generate_unique_id()
    tasks[task_id] = {"status": "in progress", "result": None}
    background_tasks.add_task(function, tasks[task_id], *args)

def get_status(tasks, task_id):
    task = tasks.get(task_id)
    if task is None:
        return { "status": "not found" }
    return task
