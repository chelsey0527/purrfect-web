import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

from utils.dashboard import display_dashboard


# API Base URL - Update this based on your Flask app's location
API_BASE_URL = 'https://techin510-final.azurewebsites.net'

def display_search_tasks():
    st.title("Search Tasks")

    with st.form("search_form"):
        col1, col2, col3, submit_col = st.columns(4)
        with col1:
            search_query = st.text_input("Task Name", key="query")
        with col2:
            date_range = st.date_input("Date Range", [])
        with col3:
            status = st.selectbox("Status", ["All", "Done", "Not Done"], key="status")
        with submit_col:
            submitted = st.form_submit_button("🔍")
    
    if submitted or not submitted:
        search_tasks(search_query, date_range, status)

def display_add_task():
    st.title("➕ Add New Task")
    add_task()
    search_tasks()

def search_tasks(query='', date_range=[], status='All'):
    response = requests.get(f"{API_BASE_URL}/tasks")
    if response.status_code == 200:
        all_tasks = response.json()
        filtered_tasks = filter_tasks(all_tasks, query, date_range, status)

        display_tasks_table(filtered_tasks)
    else:
        st.error("Failed to retrieve tasks.")

def filter_tasks(tasks, query, date_range, status):
    filtered_tasks = tasks
    if query:
        filtered_tasks = [task for task in filtered_tasks if query.lower() in task['name'].lower()]
    if date_range:
        start_date, end_date = date_range
        filtered_tasks = [task for task in filtered_tasks if start_date <= datetime.strptime(task['due_date'], "%Y-%m-%d").date() <= end_date]
    if status != 'All':
        status_bool = status == 'Done'
        filtered_tasks = [task for task in filtered_tasks if task['status'] == status_bool]
    return filtered_tasks

def toggle_task_status(task_id, current_status):
    new_status = not current_status
    response = requests.put(f"{API_BASE_URL}/tasks/{task_id}", json={'status': new_status})
    if response.status_code == 200:
        st.success("Task status updated successfully.")
    else:
        st.error(f"Failed to update task status. Error: {response.text}")

def display_tasks_table(tasks):
    st.write("Results")
    header_cols = st.columns([1.5, 1.5, 3, 2, 3, 1.5, 1.5])
    headers = ['Status', 'Task ID', 'Name', 'Category', 'Due Date', 'Toggle Status', 'Actions']
    for col, header in zip(header_cols, headers):
        col.write(header)
    
    if tasks:
        for task in tasks:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1.5, 3, 2, 3, 1.5, 1.5])
            with col1:
                st.write('✅' if task['status'] else '❌')
            with col2:
                st.write(task['task_id'])
            with col3:
                st.write(task['name'])
            with col4:
                st.write(task['category'])
            with col5:
                due_date = datetime.strptime(task['due_date'], "%a, %d %b %Y %H:%M:%S GMT")
                formatted_due_date = due_date.strftime("%a, %d %b %Y")
                st.write(formatted_due_date)
           
            with col6:
                if st.button("✏️", key=f"toggle_{task['task_id']}"):
                    toggle_task_status(task['task_id'], task['status'])
                    st.experimental_rerun()
            with col7:
                if st.button("🗑️", key=f"delete_{task['task_id']}"):
                    delete_task(task['task_id'])
    else:
        st.info("No tasks found.")

def add_task():
    with st.form("add_task_form"):

        col1, col2= st.columns(2)
        with col1:
            name = st.text_input("Task Name")
            description = st.text_area("Description")
            category = st.text_input("Category")
        with col2:
            due_date = st.date_input("Due Date", min_value=datetime.today())
            status = st.selectbox("Status", [False, True], format_func=lambda x: "✅" if x else "❌")
            submit_button = st.form_submit_button("Submit")

        if submit_button:
            if not name or not description or not category:
                st.error("Please fill in all the fields.")
                return
            task_data = {
                "name": name,
                "description": description,
                "category": category,
                "due_date": due_date.isoformat(),
                "status": status
            }
            try:
                response = requests.post(f"{API_BASE_URL}/tasks", json=task_data)
                if response.status_code == 201:
                    st.success("Task added successfully!")
                else:
                    st.error(f"Failed to add task. Error: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

def delete_task(task_id):
    response = requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
    if response.status_code == 200:
        st.success("Task deleted successfully.")
    else:
        st.error(f"Failed to delete task. Status code: {response.status_code}. Error: {response.text}")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "🔍 Search Tasks", "➕ Add New Task"])
    
    if page == "Dashboard":
        display_dashboard()
    elif page == "🔍 Search Tasks":
        display_search_tasks()
    elif page == "➕ Add New Task":
        display_add_task()

if __name__ == "__main__":
    main()
