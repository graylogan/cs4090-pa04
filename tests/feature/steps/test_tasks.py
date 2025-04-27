import os
from behave import given, when, then
from src.tasks import load_tasks, generate_unique_id, filter_tasks_by_priority, search_tasks, sort_tasks

@given("the tasks file does not exist")
def step_impl(context):
    context.test_file = "test_tasks.json"
    if os.path.exists(context.test_file):
        os.remove(context.test_file)

@when("I load the tasks")
def step_impl(context):
    context.tasks = load_tasks(file_path=context.test_file)

@then("the task list should be empty")
def step_impl(context):
    assert context.tasks == []

@given("there are 3 existing tasks with IDs 1, 2, and 5")
def step_impl(context):
    context.tasks = [{"id": 1}, {"id": 2}, {"id": 5}]

@when("I generate a unique ID")
def step_impl(context):
    context.new_id = generate_unique_id(context.tasks)

@then("the ID should be 6")
def step_impl(context):
    assert context.new_id == 6

@given("I have tasks with High and Low priority")
def step_impl(context):
    context.tasks = [
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "Low"},
        {"id": 3, "priority": "High"}
    ]

@when('I filter tasks by priority "{priority}"')
def step_impl(context, priority):
    context.filtered = filter_tasks_by_priority(context.tasks, priority)

@then("only High priority tasks should be returned")
def step_impl(context):
    assert all(task["priority"] == "High" for task in context.filtered)
    assert len(context.filtered) == 2

@given("I have tasks with various titles and descriptions")
def step_impl(context):
    context.tasks = [
        {"title": "Team meeting", "description": "Discuss roadmap"},
        {"title": "Buy groceries", "description": "Milk and eggs"},
        {"title": "Read book", "description": "Start new novel about meetings"}
    ]

@when('I search for the keyword "meeting"')
def step_impl(context):
    context.result = search_tasks(context.tasks, "meeting")

@then('I should get only tasks containing "meeting" in the title and/or description')
def step_impl(context):
    assert context.result == [
        {"title": "Team meeting", "description": "Discuss roadmap"},
        {"title": "Read book", "description": "Start new novel about meetings"}
    ]

@given('I have tasks with titles "Zebra", "apple", and "Monkey"')
def step_impl(context):
    context.tasks = [
        {"title": "Zebra"},
        {"title": "apple"},
        {"title": "Monkey"}
    ]

@when('I sort tasks by "Title"')
def step_impl(context):
    sort_tasks(context.tasks, "Title")

@then("the tasks should be in alphabetical order")
def step_impl(context):
    assert context.tasks == [
        {"title": "apple"},
        {"title": "Monkey"},
        {"title": "Zebra"}
    ]
