import unittest
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

class TestAnalyzerFull(unittest.TestCase):

    def setUp(self):
        # Набор базовых тестовых задач
        self.hard_task_1 = Task(name="Контроль", hardness="жёсткое", C=1.0, D=5.0, T=5.0)
        self.hard_task_2 = Task(name="Тревога", hardness="жёсткое", C=2.0, D=10.0, T=10.0)
        self.soft_task = Task(name="Экран", hardness="мягкое", C=4.0, D=20.0, T=20.0)
        
        # Задачи с разным соотношением D и T
        self.constrained_task = Task(name="Ограниченный", hardness="мягкое", C=1.0, D=3.0, T=5.0)
        self.arbitrary_task = Task(name="Произвольный", hardness="мягкое", C=1.0, D=10.0, T=5.0)
        self.failed_task = Task(name="Сбойная", hardness="жёсткое", C=6.0, D=5.0, T=5.0)

    # --- Тесты базовых параметров задач ---

    def test_slack_calculation(self):
        # Проверка правильности расчёта L = D - C
        self.assertEqual(slack(self.hard_task_1), 4.0)
        self.assertEqual(slack(self.failed_task), -1.0)

    def test_is_feasible(self):
        # Проверка выполнимости при L >= 0 и L < 0
        self.assertTrue(is_feasible(self.hard_task_1))
        self.assertFalse(is_feasible(self.failed_task))

    def test_deadline_types(self):
        # Проверка всех трёх вариантов соотношения D и T
        self.assertEqual(deadline_type(self.hard_task_1), "неявный (D = T)")
        self.assertEqual(deadline_type(self.constrained_task), "ограниченный (D < T)")
        self.assertEqual(deadline_type(self.arbitrary_task), "произвольный (D > T)")

    # --- Тесты классификации и метрик системы ---

    def test_classify_system(self):
        # Если есть хотя бы одна жёсткая задача -> жёсткое РВ
        tasks_with_hard = [self.soft_task, self.hard_task_1]
        self.assertEqual(classify_system(tasks_with_hard), "Система жёсткого реального времени")

        # Если все задачи мягкие -> мягкое РВ
        tasks_only_soft = [self.soft_task, self.constrained_task]
        self.assertEqual(classify_system(tasks_only_soft), "Система мягкого реального времени")

    def test_critical_task_selection(self):
        # Критической должна быть жёсткая задача с минимальным L (у hard_task_1 L=4, у hard_task_2 L=8)
        tasks = [self.hard_task_1, self.hard_task_2, self.soft_task]
        crit = critical_task(tasks)
        self.assertIsNotNone(crit)
        self.assertEqual(crit.name, "Контроль")

        # При отсутствии жёстких задач возвращается None
        self.assertIsNone(critical_task([self.soft_task]))

    def test_required_reaction_time(self):
        # R_треб выбирается как min(D) среди жёстких задач
        tasks = [self.hard_task_1, self.hard_task_2, self.soft_task]
        self.assertEqual(required_reaction_time(tasks), 5.0)

    def test_utilization_sum(self):
        # U = 1/5 + 2/10 + 4/20 = 0.2 + 0.2 + 0.2 = 0.6
        tasks = [self.hard_task_1, self.hard_task_2, self.soft_task]
        self.assertAlmostEqual(utilization(tasks), 0.6)

    def test_classify_architecture(self):
        # Проверка всех веток архитектуры
        self.assertEqual(classify_architecture(n_cpu=1, has_network=False), "Однопроцессорная система")
        self.assertEqual(classify_architecture(n_cpu=4, has_network=False), "Многопроцессорная система (4 CPU)")
        self.assertEqual(classify_architecture(n_cpu=2, has_network=True), "Распределённая система")

if __name__ == "__main__":
    unittest.main()