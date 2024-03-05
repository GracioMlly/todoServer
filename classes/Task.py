from pydantic import BaseModel
from typing import ClassVar
from datetime import date


class Task(BaseModel):
    id: str
    description: str
    priority: int
    deadline: date
    category: str | None = None

    def __init__(self, **task):
        super().__init__(**task)
        if self.category == None or self.category == "":
            self.category = "default"

    def __lt__(self, other):
        return self.deadline.toordinal() < other.deadline.toordinal()

    # Mets à jour les attributs de l'objet Task
    def update(
        self,
        id: str,
        description: str,
        priority: int,
        deadline: date,
        category: str | None = "",
    ):
        self.id = id
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.category = category
