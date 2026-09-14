import json
from pathlib import Path
from src.models import Task
from src.analyzer import (
    slack,
    is_feasible,
    deadline_type,
    classify_system,
    critical_task,
    required_reaction_time,
    utilization,
    classify_architecture,
)

def load_data(file_path: str):
    # Чтение данных из JSON файла
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    tasks = [Task(**t) for t in data["tasks"]]
    sys_info = data["system_info"]
    return tasks, sys_info

def main():
    data_file = Path(__file__).parent.parent / "data" / "tasks.json"
    tasks, sys_info = load_data(str(data_file))

    # Вывод таблицы с результатами
    print("\n" + "=" * 90)
    print(f"{'Задача':<30} | {'Класс':<8} | {'C':<4} | {'D':<4} | {'T':<4} | {'L':<5} | {'Выполнимо':<10} | {'Тип дедлайна'}")
    print("-" * 90)

    all_feasible = True
    for t in tasks:
        l_val = slack(t)
        feas = is_feasible(t)
        if not feas:
            all_feasible = False
        d_type = deadline_type(t)
        print(f"{t.name:<30} | {t.hardness:<8} | {t.C:<4.1f} | {t.D:<4.1f} | {t.T:<4.1f} | {l_val:<5.1f} | {str(feas):<10} | {d_type}")

    # Вывод аналитического заключения
    print("=" * 90)
    print(" Вывод о системе")
    print("=" * 90)

    sys_class = classify_system(tasks)
    crit = critical_task(tasks)
    r_req = required_reaction_time(tasks)
    u_val = utilization(tasks)
    arch = classify_architecture(sys_info["n_cpu"], sys_info["has_network"])

    print(f"Класс системы: {sys_class}")
    print(f"Архитектурный класс: {arch}")
    print(f"Критическая задача: {crit.name if crit else 'Отсутствует'} (L = {slack(crit) if crit else '-'} мс)")
    print(f"Требуемое время реакции R_треб: {r_req:.1f} мс")
    print(f"Коэффициент загрузки U: {u_val:.4f} ({'U <= 1 (условие выполнено)' if u_val <= 1 else 'U > 1 (перегрузка!)'})")
    print(f"Итоговая выполнимость дедлайнов: {'Все дедлайны выполнимы' if all_feasible else 'Есть нарушения дедлайнов!'}\n")

if __name__ == "__main__":
    main()