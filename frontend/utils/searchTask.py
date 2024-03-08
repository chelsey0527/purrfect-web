import streamlit as st
import requests
from datetime import datetime

API_BASE_URL = 'http://127.0.0.1:5000'

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