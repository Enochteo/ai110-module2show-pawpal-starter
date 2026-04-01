import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age_years = st.number_input("Pet age (years)", min_value=0, max_value=30, value=3)

# Initialize owner and pet in session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
    st.session_state.pet = Pet(name=pet_name, species=species, age_years=int(age_years))
    st.session_state.owner.add_pet(st.session_state.pet)

st.markdown("### Add Tasks")
st.caption("Define tasks for your pet and generate a schedule.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task description", value="Morning walk")
with col2:
    task_time = st.text_input("Time", value="08:00 AM")
with col3:
    task_frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly", "as needed"])

if st.button("Add task"):
    task = Task(description=task_title, time=task_time, frequency=task_frequency)
    st.session_state.pet.add_task(task)
    st.success(f"Added task: {task_title}")

if st.session_state.pet.tasks:
    st.write("Current tasks:")
    task_data = [
        {
            "Description": task.description,
            "Time": task.time,
            "Frequency": task.frequency,
            "Completed": task.completed,
        }
        for task in st.session_state.pet.tasks
    ]
    st.table(task_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Generate Schedule")
st.caption("Organize and view all tasks for your pet.")

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    organized_tasks = scheduler.organize_tasks()
    
    if organized_tasks:
        st.success("Schedule generated!")
        st.markdown(f"**{scheduler.owner.name}'s Schedule for {st.session_state.pet.name}**")
        
        task_data = [
            {
                "Description": task.description,
                "Time": task.time,
                "Frequency": task.frequency,
                "Status": "✓ Completed" if task.completed else "Pending",
            }
            for task in organized_tasks
        ]
        st.table(task_data)
    else:
        st.info("No tasks to schedule. Add tasks above first.")
