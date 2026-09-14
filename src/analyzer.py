from typing import List, Optional
from src.models import Task

def slack(task: Task) -> float:
    #Запас времени задачи L = D - C.
    return task.D - task.C

def is_feasible(task: Task) -> bool:
    #Признак выполнимости дедлайна (L >= 0).
    return slack(task) >= 0

def deadline_type(task: Task) -> str:
    #Тип дедлайна по соотношению D и T.
    if task.D == task.T:
        return "неявный (D = T)"
    elif task.D < task.T:
        return "ограниченный (D < T)"
    else:
        return "произвольный (D > T)"

def classify_system(tasks: List[Task]) -> str:
    #Класс системы: жёсткое РВ, если есть хотя бы одна жёсткая задача, иначе мягкое.
    for task in tasks:
        if task.hardness.lower() == "жёсткое":
            return "Система жёсткого реального времени"
    return "Система мягкого реального времени"

def critical_task(tasks: List[Task]) -> Optional[Task]:
    #Критическая задача — с наименьшим запасом среди жёстких.
    hard_tasks = [t for t in tasks if t.hardness.lower() == "жёсткое"]
    if not hard_tasks:
        return None
    return min(hard_tasks, key=slack)

def required_reaction_time(tasks: List[Task]) -> float:
    #Требуемое время реакции системы по жёстким задачам (при отсутствии — по всем).
    hard_tasks = [t for t in tasks if t.hardness.lower() == "жёсткое"]
    target_tasks = hard_tasks if hard_tasks else tasks
    return min(t.D for t in target_tasks)

def utilization(tasks: List[Task]) -> float:
    #Коэффициент загрузки U = sum(C_i / T_i).
    return sum(t.C / t.T for t in tasks)

def classify_architecture(n_cpu: int, has_network: bool) -> str:
    #Архитектурный класс системы по числу процессорных ядер и наличию сети.
    if has_network:
        return "Распределённая система"
    elif n_cpu > 1:
        return f"Многопроцессорная система ({n_cpu} CPU)"
    else:
        return "Однопроцессорная система"