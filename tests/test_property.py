import pytest
from hypothesis import given, strategies as st
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tasks import (
    generate_unique_id,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    search_tasks,
    mark_all_tasks,
    sort_tasks
)

# Test generate_unique_id()
@given(st.lists(st.integers(min_value=1, max_value=1000).map(lambda x: {"id": x})))
def test_generate_unique_id_is_unique(task_list):
    if task_list:
        expected = max(t["id"] for t in task_list) + 1
    else:
        expected = 1
    assert generate_unique_id(task_list) == expected

# Test filter_tasks_by_priority()
@given(
    st.lists(
        st.fixed_dictionaries({
            "id": st.integers(),
            "priority": st.sampled_from(["High", "Medium", "Low"])
        })
    ),
    st.sampled_from(["High", "Medium", "Low"])
)
def test_filter_tasks_by_priority_only_matches(tasks, priority):
    filtered = filter_tasks_by_priority(tasks, priority)
    assert all(task["priority"] == priority for task in filtered)

# Test filter_tasks_by_category()
@given(
    st.lists(
        st.fixed_dictionaries({
            "id": st.integers(),
            "category": st.sampled_from(["Personal", "School", "Work", "Other"])
        })
    ),
    st.sampled_from(["Personal", "School", "Work", "Other"])
)
def test_filter_tasks_by_category_only_matches(tasks, category):
    filtered = filter_tasks_by_category(tasks, category)
    assert all(task["category"] == category for task in filtered)

# Test search_tasks()
@given(
    st.lists(
        st.fixed_dictionaries({
            "title": st.text(),
            "description": st.text()
        })
    ),
    st.text()
)
def test_search_tasks_matches_title_or_description(tasks, query):
    results = search_tasks(tasks, query)
    for task in results:
        assert query.lower() in task["title"].lower() or query.lower() in task["description"].lower()

# Test mark_all_tasks()
@given(
    st.lists(st.fixed_dictionaries({
        "completed": st.booleans()
    })),
    st.booleans()
)
def test_mark_all_tasks_sets_completion(tasks, flag):
    mark_all_tasks(tasks, complete=flag)
    assert all(task["completed"] == flag for task in tasks)
