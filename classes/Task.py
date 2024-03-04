from pydantic import BaseModel
from datetime import date


class Task(BaseModel):
    id: str
    description: str
    priority: int
    deadline: date
    category: str | None = ""

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
