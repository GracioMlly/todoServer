from pydantic import BaseModel
from classes.Task import Task
from typing import ClassVar
from uuid import uuid4


class Category(BaseModel):
    id: str | None = None
    name: str
    tasks: list[Task] | None = None

    all_categories_name: ClassVar[list[str]] = []

    def __init__(self, **category):
        super().__init__(**category)
        self.tasks = []
        if self.id == None:
            self.id = str(uuid4())

    def add_task(self, task: Task):
        self.tasks.append(task)

    def delete_task(self, value: Task | str):
        try:
            if type(value) is str:
                task = next(task for task in self.tasks if task.id == value)
                self.tasks.remove(task)
            else:
                self.tasks.remove(value)
        except Exception as error:
            print(error)
