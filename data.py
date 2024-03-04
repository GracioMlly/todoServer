from classes.Task import Task
from queue import PriorityQueue, LifoQueue

tasksList : list[Task] = []
tasksByDeadline = PriorityQueue()
tasksByPriorityOrder = LifoQueue()