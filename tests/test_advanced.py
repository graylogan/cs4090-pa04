import pytest
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tasks import (
    generate_unique_id,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    search_tasks,
    sort_tasks
)

# ---------- Fixture ----------

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Task A", "priority": "High", "category": "Work", "description": "Send email"},
        {"id": 2, "title": "Task B", "priority": "Low", "category": "Personal", "description": "Go for a run"},
        {"id": 3, "title": "Task C", "priority": "Medium", "category": "School", "description": "Finish Homework"},
    ]

# ---------- Tests ----------

@pytest.mark.parametrize("priority,expected_count", [
    ("High", 1),
    ("Low", 1),
    ("Medium", 1),
    ("Urgent", 0)
])
def test_filter_tasks_by_priority(sample_tasks, priority, expected_count):
    filtered = filter_tasks_by_priority(sample_tasks, priority)
    assert len(filtered) == expected_count


@pytest.mark.parametrize("category,expected_count", [
    ("Work", 1),
    ("Personal", 1),
    ("School", 1),
    ("Other", 0)
])
def test_filter_tasks_by_category(sample_tasks, category, expected_count):
    filtered = filter_tasks_by_category(sample_tasks, category)
    assert len(filtered) == expected_count


@pytest.mark.parametrize("query,expected_ids", [
    ("Task", [1, 2, 3]),
    ("task a", [1]),
    ("homeWoRk", [3]),
    ("xyz", [])
])
def test_search_tasks(sample_tasks, query, expected_ids):
    result = search_tasks(sample_tasks, query)
    result_ids = [t["id"] for t in result]
    assert result_ids == expected_ids


def test_sort_tasks_by_title(sample_tasks):
    sort_tasks(sample_tasks, "Title")
    ids = [task["id"] for task in sample_tasks]
    assert ids == [1, 2, 3]
