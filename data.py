from classes.Task import Task
from classes.Category import Category
from queue import PriorityQueue, LifoQueue

# Liste des tâches
tasksList : list[Task] = []

# La file des tâches par date de priorité
tasksByDeadline = PriorityQueue()

# La pile des tâches par ordre de priorité
tasksByPriorityOrder = LifoQueue()

# La liste des catégories
categoriesList: list[Category] = [] 
