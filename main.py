from fastapi import FastAPI
from classes.Task import Task
from classes.Category import Category
from queue import PriorityQueue, LifoQueue
from uuid import uuid4

from data import tasksList, tasksByDeadline, tasksByPriorityOrder, categoriesList

app = FastAPI()

###############################################################################################
""" Gestion des tâches """


""" Pour récupérer les tâches """


@app.get("/tasks")
async def get_tasks(filter: str | None = None):
    try:
        if filter == "date":
            return sorted(
                tasksByDeadline.queue, key=lambda task: task.deadline, reverse=True
            )
        elif filter == "order":
            return sorted(
                tasksByPriorityOrder.queue, key=lambda task: task.priority, reverse=True
            )
        else:
            return tasksList
    except Exception as error:
        print(error)
        return {"message": f"le filtrage n'a pas pu avoir lieu"}


""" Pour créer une tâche """


@app.post("/tasks")
async def create_task(task: Task):
    try:
        newTask = Task(**task.model_dump())
        tasksList.append(newTask)

        tasksByDeadline.put_nowait(newTask)
        tasksByPriorityOrder.put_nowait(newTask)

        category_manager(newTask, categoriesList)
        return {"message": "la tâche a été ajoutée", "tâche": newTask}
    except Exception as error:
        print(error)
        return {"message": "la tâche n'a pas été crée"}


""" Pour modifier une tâche """


@app.put("/tasks/{taskId}")
async def update_task(taskId: str, task: Task):
    try:
        taskToUpdate = next(task for task in tasksList if task.id == taskId)
        if taskToUpdate.category != task.category:
            update_task_category(taskToUpdate, task, categoriesList)
        taskToUpdate.update(**task.model_dump())
        return {"message": "la tâche a été mise à jour", "tâche": taskToUpdate}
    except Exception as error:
        print(error)
        return {"message": "la tâche n'a pas été mise à jour"}


""" Pour supprimer une tâche """


@app.delete("/tasks/{taskId}")
async def delete_task(taskId: str):
    global tasksList
    try:
        taskToDelete = next(task for task in tasksList if task.id == taskId)
        tasksList.remove(taskToDelete)
        priority_lists_updater(tasksByDeadline)
        priority_lists_updater(tasksByPriorityOrder)
        category_list_updater(taskToDelete, categoriesList)
        return {"message": "la tâche a été supprimée", "tâche": taskToDelete}
    except Exception as error:
        print(error)
        return {"message": f"la tâche avec l'Id {taskId} n'existe pas"}


###############################################################################################
""" Gestion des catégories """

""" Pour récupérer la liste de catégories """


@app.get("/categories")
async def get_categories():
    return categoriesList


""" Pour créer une catégorie """


@app.post("/categories")
async def create_task(category: Category):
    try:
        newCategory = Category(**category.model_dump())
        isPresent = does_this_category_already_exist(newCategory.name, categoriesList)
        if isPresent:
            return {"message": f"La catégorie {newCategory.name} existe déjà"}
        else:
            Category.all_categories_name.append(category.name)
            categoriesList.append(newCategory)
            return {"message": "la catégorie a été ajoutée", "catégorie": newCategory}
    except Exception as error:
        print(error)
        return {"message": "La catégorie n'a pas été crée"}


@app.delete("/categories/{categoryId}")
async def delete_category(categoryId: str):
    try:
        categoryToDelete = next(
            category for category in categoriesList if category.id == categoryId
        )
        for task in categoryToDelete.tasks:
            tasksList.remove(task)
        priority_lists_updater(tasksByDeadline)
        priority_lists_updater(tasksByPriorityOrder)

        categoriesList.remove(categoryToDelete)

        return {"message": "la catégorie a été supprimée", "catégorie": categoryToDelete}
    except Exception as error:
        print(error)
        return {"message": "la catégorie n'a pas pu être supprimée"}


###############################################################################################

""" Fonctions utilitaires """


def priority_lists_updater(structure: PriorityQueue | LifoQueue):
    structure.queue = tasksList.copy()

def category_list_updater(task: Task, categoriesList: list[Category]):
    try:
        categoryToUpdate = next(category for category in categoriesList if category.name == task.category)
        categoryToUpdate.delete_task(task)
    except Exception as error:
        print(error)

def category_manager(task: Task, categoriesList: list[Category]):
    try:
        if task.category in Category.all_categories_name:
            category = next(
                category
                for category in categoriesList
                if category.name == task.category
            )
            category.add_task(task)
        else:
            Category.all_categories_name.append(task.category)
            category = Category(id=str(uuid4()), name=task.category)
            category.add_task(task)
            categoriesList.append(category)
    except Exception as error:
        print(error)
        return {"message": "Complications dans la gestion des catégories"}


def does_this_category_already_exist(name: str, categoriesList: list[Category]):
    try:
        category = next(
            category for category in categoriesList if category.name == name
        )
        if category:
            return True
    except Exception as error:
        print("Catégorie non trouvée", error)
        return False


def update_task_category(
    taskToUpdate: Task, task: Task, categoriesList: list[Category]
):
    try:
        taskId = taskToUpdate.id
        oldCategory = next(
            category
            for category in categoriesList
            if category.name == taskToUpdate.category
        )

        if does_this_category_already_exist(task.category, categoriesList):
            newCategory = next(
                category
                for category in categoriesList
                if category.name == task.category
            )
            newCategory.add_task(taskToUpdate)
        else:
            category_manager(task, categoriesList)

        oldCategory.delete_task(taskId)

    except Exception as error:
        print(error)
