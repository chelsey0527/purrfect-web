import pandas as pd
import requests
import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

API_BASE_URL = 'https://techin510-final.azurewebsites.net'

def fetch_tasks():
    response = requests.get(f"{API_BASE_URL}/tasks")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Failed to retrieve tasks.")
        return pd.DataFrame()

df = fetch_tasks()
df['due_date'] = pd.to_datetime(df['due_date'])
df['status'] = df['status'].astype(bool)

def plot_daily_task_counts(df):
    if not df.empty:
        df['due_date'] = pd.to_datetime(df['due_date'])  
        daily_counts = df.groupby(df['due_date'].dt.date).size()
        plt.figure(figsize=(10, 6))
        daily_counts.plot(kind='bar')
        plt.title('Overall Daily Task Counts')
        plt.xlabel('Date')
        plt.ylabel('Number of Tasks')
        plt.xticks(rotation=45)
        st.pyplot(plt)

def plot_last_week_task_status(df):
    if not df.empty:
        last_week = datetime.now() - timedelta(days=7)
        last_week_tasks = df[df['due_date'].dt.date >= last_week.date()]
        status_counts = last_week_tasks.groupby('status').size()
        status_counts.index = ['Not Finished', 'Finished']
        plt.figure(figsize=(10, 6))
        status_counts.plot(kind='bar', color=['red', 'green'])
        plt.title("Last Week's Task Status")
        plt.xlabel('Status')
        plt.ylabel('Number of Tasks')
        plt.xticks(rotation=0)
        st.pyplot(plt)

def plot_category_proportions(df):
    if not df.empty:
        category_counts = df['category'].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')
        plt.title('Task Category')
        st.pyplot(plt)

def display_dashboard():
    st.title("Dashboard")
    df = fetch_tasks()

    if not df.empty:
        plot_daily_task_counts(df)
        plot_category_proportions(df)
        plot_last_week_task_status(df) 
           
    # Auto-update every 10 minutes
    if 'last_update' not in st.session_state or datetime.now() - st.session_state.last_update > timedelta(minutes=10):
        st.session_state.last_update = datetime.now()
        st.experimental_rerun()