from datetime import datetime

tasks_storage: dict[int, list[dict]] = {}

task_id_counter = 0

def add_task(user_id: int, title: str, deadline: datetime | None) -> dict:
    global task_id_counter
    task_id_counter += 1

    task = {
        "id": task_id_counter,
        "title": title,
        "deadline": deadline,
        "done": False,
        "created_at": datetime.now()
    }

    if user_id not in tasks_storage:
        tasks_storage[user_id] = []

    tasks_storage[user_id].append(task)
    return task

def get_tasks(user_id: int) -> list[dict]:
    return tasks_storage.get(user_id, [])

def mark_done(user_id: int, task_id: int) -> bool:
    for task in tasks_storage.get(user_id, []):
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False