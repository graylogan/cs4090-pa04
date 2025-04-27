import pytest
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import copy
import src.tasks as tsks


def test_mark_all_tasks():
    tasks = [
        {"title": "Task 1", "completed": True},
        {"title": "Task 2", "completed": False},
        {"title": "Task 3", "completed": True},
    ]

    # test mark all true
    complete_tasks = copy.deepcopy(tasks)
    tsks.mark_all_tasks(complete_tasks, True)
    assert all(task["completed"] for task in complete_tasks)

    # test mark all false
    incomplete_tasks = copy.deepcopy(tasks)
    tsks.mark_all_tasks(incomplete_tasks, complete=False)
    assert not any(task["completed"] for task in incomplete_tasks)

    # test empty
    empty = []
    tsks.mark_all_tasks(empty)
    assert empty == []


def test_update_task():
    task = {
        "id": 2,
        "title": "Go to Store",
        "description": "Buy milk and bread",
        "priority": "Medium",
        "category": "Personal",
        "due_date": "2025-04-29",
        "completed": False,
        "created_at": "2025-04-26 18:35:43",
    }

    # test updating with same values does not change
    task_copy = copy.deepcopy(task)
    tsks.update_task(
        task_copy,
        task_copy["title"],
        task_copy["description"],
        task_copy["priority"],
        task_copy["category"],
        task_copy["due_date"],
    )
    assert task_copy == task

    # test updated values change
    tsks.update_task(
        task, "Travel to Store", "Buy eggs and butter", "High", "Work", "2025-05-10"
    )
    assert task == {
        "id": 2,
        "title": "Travel to Store",
        "description": "Buy eggs and butter",
        "priority": "High",
        "category": "Work",
        "due_date": "2025-05-10",
        "completed": False,
        "created_at": "2025-04-26 18:35:43",
    }


def test_sort_tasks():
    tasks = [
        {
            "id": 1,
            "title": "Task 1",
            "priority": "Low",
            "due_date": "2025-04-16",
        },
        {
            "id": 2,
            "title": "Task 2",
            "priority": "Medium",
            "due_date": "2025-04-14",
        },
        {
            "id": 3,
            "title": "Task 3",
            "priority": "High",
            "due_date": "2025-04-15",
        },
    ]
    # test priority
    tsks.sort_tasks(tasks, "Priority")
    assert tasks[0]["id"] == 3
    # test Title
    tsks.sort_tasks(tasks, "Title")
    assert tasks[0]["id"] == 1
    # test Due Date
    tsks.sort_tasks(tasks, "Due Date")
    assert tasks[0]["id"] == 2
