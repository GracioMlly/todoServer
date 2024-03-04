from fastapi import FastAPI
from classes.Task import Task
from queue import PriorityQueue, LifoQueue
from data import tasksList, tasksByDeadline, tasksByPriorityOrder

app = FastAPI()

###############################################################################################

# Tâches


# Pour récupérer la liste des tâches
@app.get("/")
async def get_tasks() -> list[Task]:
    return tasksList


@app.get("/tasks")
async def get_tasks(filter: str | None = None) -> list[Task]:
    try:
        if filter == "date":
            return convert_To_List(tasksByDeadline, "date")
        if filter == "order":
            sortedList = sorted(
                tasksByPriorityOrder.queue, key=lambda x: x.priority, reverse=True
            )
            # tasksByPriorityOrder.queue.sort(key=lambda task: task.priority)
            return sortedList
        else:
            return tasksList
    except Exception as error:
        print(error)
        return {"message": f"le filtrage n'a pas pu avoir lieu"}


# Pour créer une tâche
@app.post("/tasks")
async def create_task(task: Task):
    try:
        newTask = Task(**task.model_dump())
        tasksList.append(task)
        tasksByDeadline.put_nowait((task.deadline, task))
        tasksByPriorityOrder.put_nowait(task)
        print(tasksByPriorityOrder.qsize())
        return {"message": "la tâche a été ajoutée", "tâche": task}
    except Exception as error:
        print(error)
        return {"message": "la tâche n'a pas été crée"}


# Pour mettre à jour une tâche
@app.put("/tasks/{taskId}")
async def update_task(taskId: str, task: Task):
    try:
        taskToUpdate = next(task for task in tasksList if task.id == taskId)
        taskToUpdate.update(**task.model_dump())
        return {"message": "la tâche a été mise à jour", "tâche": taskToUpdate}
    except Exception as error:
        print(error)
        return {"message": "la tâche n'a pas été mise à jour"}


# Pour supprimer une tâche
@app.delete("/tasks/{taskId}")
async def delete_task(taskId: str):
    global tasksList
    try:
        taskToDelete = next(task for task in tasksList if task.id == taskId)
        tasksList = [task for task in tasksList if task != taskToDelete]
        priority_lists_updater(tasksByDeadline)
        return {"message": "la tâche a été supprimée", "tâche": taskToDelete}
    except Exception as error:
        print(error)
        return {"message": f"la tâche avec l'Id {taskId} n'existe pas"}


###############################################################################################


def convert_To_List(structure: PriorityQueue | LifoQueue, type: str = ""):
    if type == "date":
        list = [data[1] for data in structure.queue]
        return list
    else:
        list = [data for data in structure.queue]
        return list


def priority_lists_updater(structure: PriorityQueue | LifoQueue):
    structure.queue.clear()
    for task in tasksList:
        structure.put(task)


def sort_priority(structure: LifoQueue):
    pass
