import streamlit as st
import pandas as pd
import subprocess
from datetime import datetime
from tasks import (
    load_tasks,
    save_tasks,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    generate_unique_id,
    search_tasks,
    mark_all_tasks,
    update_task,
    sort_tasks
)

# NOTES:
# Potential bug with task ID (solution already implemented)
# Fixed overdue task bug with no due_date 

def run_command(command):
    with st.spinner(f"Running: `{command}`..."):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        st.code(result.stdout + result.stderr, language='bash')
        if result.returncode == 0:
            st.success("✅ Success")
        else:
            st.error("❌ Failed")

def main():
    st.title("To-Do Application")
    if st.button("Run Basic Unit Tests"):
        run_command("pytest tests/test_basic.py")
    if st.button("Run Parameterized Tests"):
        run_command("pytest tests/test_advanced.py")
    if st.button("Check Test Coverage"):
        run_command("pytest --cov=src.tasks")
    if st.button("Generate HTML Report"):
        run_command("pytest --html=report.html")
    if st.button("Run with Mock (trace config)"):
        run_command("pytest --trace-config")
    if st.button("Run BDD Tests"):
        run_command("behave tests/feature/")
    if st.button("Run Property Tests"):
        run_command("pytest tests/test_property.py/")
    

    # Load existing tasks from JSON file
    tasks = load_tasks()

    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")

    # Task creation form in sidebar
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox(
            "Category", ["Work", "Personal", "School", "Other"]
        )
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")

        if (
            submit_button and task_title
        ):  # append to task list and update JSON file on submit with a title
            new_task = {
                #"id": len(tasks) + 1,  # BUGGY CODE
                "id": generate_unique_id(tasks),  # <- FIXED HERE
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")

    # Main area to display tasks
    st.header("Your Tasks")

    # Filter options
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"] + list(set([task["category"] for task in tasks])),
        )
    with col2:
        filter_priority = st.selectbox(
            "Filter by Priority", ["All", "High", "Medium", "Low"]
        )
    with col3:
        filter_query = st.text_input("Filter by Search", "")
    with col4:
        sort_by = st.selectbox(
            "Sort tasks by",
            ["None", "Due Date", "Priority", "Title"]
        )


    col1, col2, col3 = st.columns(3)
    with col1:
        show_completed = st.checkbox("Show Completed Tasks")
    with col2:
        if st.button("Mark All Complete"):
            mark_all_tasks(tasks)
            save_tasks(tasks)
    with col3:
        if st.button("Mark All Incomplete"):
            mark_all_tasks(tasks, False)
            save_tasks(tasks)

    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    filtered_tasks = search_tasks(filtered_tasks, filter_query)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # sort tasks
    sort_tasks(filtered_tasks, sort_by)


    # check for edit
    editing_task_id = st.session_state.get("editing_task_id")

    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(
                f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}"
            )
        with col2:
            if st.button(
                "Complete" if not task["completed"] else "Undo",
                key=f"complete_{task['id']}",
            ):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)  # Update JSON on Task comlpete/undo
                        st.rerun()  # Run main again?
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)  # update JSON on delete
                st.rerun()  # Reload page
            if task["id"] != editing_task_id and st.button("Edit", key=f"edit_{task['id']}"):
                st.session_state["editing_task_id"] = task["id"]
                st.rerun()

        # if editing task
        if task["id"] == editing_task_id:
            with st.form(f"edit_form_{task['id']}"):
                new_title = st.text_input("Title", task["title"])
                new_description = st.text_area("Description", task["description"])
                new_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task["priority"]))
                new_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"], index=["Work", "Personal", "School", "Other"].index(task["category"]))
                new_due_date = st.date_input("Due Date", task["due_date"])
                submit_edit = st.form_submit_button("Save Changes")
                cancel_edit = st.form_submit_button("Cancel")

                if submit_edit:
                    update_task(task, new_title, new_description, new_priority, new_category, new_due_date)
                    save_tasks(tasks)
                    st.session_state["editing_task_id"] = None
                    st.rerun()

                if cancel_edit:
                    st.session_state["editing_task_id"] = None
                    st.rerun()

if __name__ == "__main__":
    main()
