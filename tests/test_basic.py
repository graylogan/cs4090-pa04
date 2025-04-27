import pytest
import sys
import os
from datetime import timedelta, datetime

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.tasks as tsks


def test_generate_unique_id_empty():
    tasks = []
    assert tsks.generate_unique_id(tasks) == 1


def test_generate_unique_id_non_empty():
    tasks = [
        {"id": 1, "title": "Task 1"},
        {"id": 2, "title": "Task 2"},
        {"id": 5, "title": "Task 5"},
    ]
    assert tsks.generate_unique_id(tasks) == 6


def test_filter_tasks_by_priority():
    tasks = [
        {"title": "Task 1", "priority": "High"},
        {"title": "Task 2", "priority": "Low"},
        {"title": "Task 3", "priority": "Medium"},
        {"title": "Task 4", "priority": "High"},
        {"title": "Task 5"},  # Missing 'priority' key
    ]

    high_priority = tsks.filter_tasks_by_priority(tasks, "High")
    assert high_priority == [
        {"title": "Task 1", "priority": "High"},
        {"title": "Task 4", "priority": "High"},
    ]

    medium_priority = tsks.filter_tasks_by_priority(tasks, "Medium")
    assert medium_priority == [{"title": "Task 3", "priority": "Medium"}]

    low_priority = tsks.filter_tasks_by_priority(tasks, "Low")
    assert low_priority == [{"title": "Task 2", "priority": "Low"}]

    no_priority = tsks.filter_tasks_by_priority(tasks, "Urgent")
    assert no_priority == []


def test_filter_tasks_by_category():
    tasks = [
        {"title": "Task 1", "category": "Work"},
        {"title": "Task 2", "category": "Personal"},
        {"title": "Task 3", "category": "Work"},
        {"title": "Task 4", "category": "Errands"},
        {"title": "Task 5"},  # No category
    ]

    work_tasks = tsks.filter_tasks_by_category(tasks, "Work")
    assert work_tasks == [
        {"title": "Task 1", "category": "Work"},
        {"title": "Task 3", "category": "Work"},
    ]

    personal_tasks = tsks.filter_tasks_by_category(tasks, "Personal")
    assert personal_tasks == [{"title": "Task 2", "category": "Personal"}]

    errands_tasks = tsks.filter_tasks_by_category(tasks, "Errands")
    assert errands_tasks == [{"title": "Task 4", "category": "Errands"}]

    no_match = tsks.filter_tasks_by_category(tasks, "Fitness")
    assert no_match == []


def test_filter_tasks_by_completion():
    tasks = [
        {"title": "Task 1", "completed": True},
        {"title": "Task 2", "completed": False},
        {"title": "Task 3", "completed": True},
        {"title": "Task 4"},  # No 'completed' key
        {"title": "Task 5", "completed": False},
    ]

    completed_tasks = tsks.filter_tasks_by_completion(tasks, completed=True)
    assert completed_tasks == [
        {"title": "Task 1", "completed": True},
        {"title": "Task 3", "completed": True},
    ]

    incomplete_tasks = tsks.filter_tasks_by_completion(tasks, completed=False)
    assert incomplete_tasks == [
        {"title": "Task 2", "completed": False},
        {"title": "Task 5", "completed": False},
    ]


def test_search_tasks():
    tasks = [
        {"title": "Buy groceries", "description": "Milk, Eggs, Bread"},
        {"title": "Call Mom", "description": "Her birthday is coming up"},
        {"title": "Workout", "description": "Leg day at the gym"},
        {"title": "Read book", "description": "Finish the sci-fi novel"},
        {"title": "Email the boss", "description": "Send project update"},
    ]

    # Case-insensitive title match
    results = tsks.search_tasks(tasks, "call")
    assert results == [
        {"title": "Call Mom", "description": "Her birthday is coming up"}
    ]

    # Case-insensitive description match
    results = tsks.search_tasks(tasks, "bread")
    assert results == [{"title": "Buy groceries", "description": "Milk, Eggs, Bread"}]

    # Case-insensitive query
    results = tsks.search_tasks(tasks, "bOoK")
    assert results == [
        {"title": "Read book", "description": "Finish the sci-fi novel"},
    ]

    # Multiple Matches
    results = tsks.search_tasks(tasks, "the")
    assert results == [
        {"title": "Workout", "description": "Leg day at the gym"},
        {"title": "Read book", "description": "Finish the sci-fi novel"},
        {"title": "Email the boss", "description": "Send project update"},
    ]

    # No match
    results = tsks.search_tasks(tasks, "vacation")
    assert results == []

    # Empty query returns all tasks
    results = tsks.search_tasks(tasks, "")
    assert results == tasks


def test_get_overdue_tasks():
    today = datetime.now().date()
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    today = today.strftime("%Y-%m-%d")

    tasks = [
        {"title": "Task 1", "due_date": yesterday, "completed": False},  # Overdue
        {"title": "Task 2", "due_date": yesterday, "completed": True},  # Completed
        {"title": "Task 3", "due_date": yesterday},  # Should assumed incomplete
        {"title": "Task 4", "due_date": today, "completed": False},  # Due today
        {"title": "Task 5", "due_date": tomorrow, "completed": False},  # Not overdue
        {"title": "Task 6"},  # No due_date or completed should not be overdue
    ]

    overdue = tsks.get_overdue_tasks(tasks)

    assert overdue == [
        {"title": "Task 1", "due_date": yesterday, "completed": False},
        {"title": "Task 3", "due_date": yesterday},
    ]


# helper function for testing save and load tasks
def remove_file(file_path: str):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.", file=sys.stderr)
    except PermissionError:
        print(f"Permission denied to delete '{file_path}'.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


def test_save_and_load_tasks():
    tasks = [
        {
            "id": 1,
            "title": "Task 1",
            "description": "Desc for Task 1",
            "priority": "Low",
            "category": "Personal",
            "due_date": "2025-04-26",
            "completed": False,
            "created_at": "2025-04-26 13:52:52",
        },
        {
            "id": 2,
            "title": "Task 2",
            "description": "Desc for Task 2",
            "priority": "Medium",
            "category": "Work",
            "due_date": "2025-04-29",
            "completed": True,
            "created_at": "2025-04-26 13:53:03",
        },
        {
            "id": 3,
            "title": "No Desc Task",
            "description": "",
            "priority": "High",
            "category": "Other",
            "due_date": "2025-04-26",
            "completed": False,
            "created_at": "2025-04-26 13:53:59",
        },
    ]
    test_file = "test_save_and_load_tasks_file.json"
    remove_file(test_file)  # remove in case already exists
    tsks.save_tasks(tasks, test_file)
    retrieved_tasks = tsks.load_tasks(test_file)
    assert retrieved_tasks == tasks
    remove_file(test_file)  # clean up


def test_load_tasks_exceptions():
    # check corrupted exception
    test_file = "test_load_tasks_corrupted_file"
    with open(test_file, "w") as file:
        file.write("!?<Corrupted JSON>?!*")
    tasks = tsks.load_tasks(test_file)
    assert tasks == []
    remove_file(test_file)

    # check file not found exception
    test_file = "test_does_not_exist_hf38947ydfu398hf3"
    remove_file(test_file)  # make sure file doesn't exist
    tasks = tsks.load_tasks(test_file)
    assert tasks == []
