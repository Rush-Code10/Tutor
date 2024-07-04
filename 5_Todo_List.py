import streamlit as st
import datetime

st.set_page_config(
    page_title="Todo List",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.header("Todo List", divider="grey", anchor=False)
# Initialize session state for storing tasks if not already done
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

# Function to add a new task
def add_task():
    task = st.session_state['new_task']
    if task:
        st.session_state['tasks'].append({"task": task, "completed": False, "date_added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        st.session_state['new_task'] = ""

# Function to mark a task as completed
def complete_task(index):
    st.session_state['tasks'][index]["completed"] = not st.session_state['tasks'][index]["completed"]

# Function to delete a task
def delete_task(index):
    del st.session_state['tasks'][index]

# Input box for new task
st.text_input("Add a new task", key='new_task', on_change=add_task)

# Display existing tasks
st.subheader("Tasks")
for i, task in enumerate(st.session_state['tasks']):
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    col1.write(f"{task['task']} ({task['date_added']})")
    col2.button("Complete" if not task['completed'] else "Undo", key=f"complete_{i}", on_click=complete_task, args=(i,))
    col3.button("Delete", key=f"delete_{i}", on_click=delete_task, args=(i,))
    col4.write("✅" if task['completed'] else "❌")
