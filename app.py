import streamlit as st
from datetime import datetime

from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Plan and manage pet-care tasks with scheduling, filtering, and conflict warnings.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** helps a pet owner keep routines on track.
Add tasks, mark progress, and review a sorted schedule with time-conflict alerts.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
This demo currently supports:
- Adding tasks in HH:MM or AM/PM format
- Sorting tasks chronologically via Scheduler
- Filtering pending vs completed tasks via Scheduler
- Conflict detection with non-crashing warning messages
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age_years = st.number_input("Pet age (years)", min_value=0, max_value=30, value=3)


def normalize_time_input(raw_time: str) -> str | None:
    """Normalize user time input to HH:MM format for Scheduler methods."""
    value = raw_time.strip()
    accepted_formats = ["%H:%M", "%I:%M %p", "%I:%M%p"]
    for fmt in accepted_formats:
        try:
            return datetime.strptime(value, fmt).strftime("%H:%M")
        except ValueError:
            continue
    return None

# Initialize owner and pet in session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
    st.session_state.pet = Pet(name=pet_name, species=species, age_years=int(age_years))
    st.session_state.owner.add_pet(st.session_state.pet)

st.session_state.owner.name = owner_name
st.session_state.pet.name = pet_name
st.session_state.pet.species = species
st.session_state.pet.age_years = int(age_years)

st.markdown("### Add Tasks")
st.caption("Define tasks for your pet and generate a schedule.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task description", value="Morning walk")
with col2:
    task_time = st.text_input("Time", value="08:00")
with col3:
    task_frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly", "as needed"])

if st.button("Add task"):
    normalized_time = normalize_time_input(task_time)
    if not normalized_time:
        st.warning("Invalid time format. Use HH:MM (e.g., 08:00) or AM/PM (e.g., 8:00 AM).")
    else:
        task = Task(description=task_title.strip(), time=normalized_time, frequency=task_frequency)
        st.session_state.pet.add_task(task)
        st.success(f"Added task: {task_title} at {normalized_time}")

scheduler = Scheduler(st.session_state.owner)

if st.session_state.pet.tasks:
    st.write("Current tasks (sorted):")
    sorted_tasks = scheduler.sort_by_time(include_completed=True)
    task_data = [
        {
            "Description": task.description,
            "Time": task.time,
            "Frequency": task.frequency,
            "Completed": task.completed,
        }
        for task in sorted_tasks
    ]
    st.table(task_data)

    st.markdown("### Mark Task Complete")
    pending_tasks = scheduler.filter_tasks(completed=False, pet_name=st.session_state.pet.name)
    if pending_tasks:
        task_options = [f"{task.time} | {task.description}" for task in pending_tasks]
        selected_option = st.selectbox("Pending tasks", options=task_options)
        if st.button("Mark selected task complete"):
            selected_description = selected_option.split(" | ", 1)[1]
            was_marked = scheduler.mark_task_completed(st.session_state.pet.name, selected_description)
            if was_marked:
                st.success("Task marked complete. Recurring tasks are auto-recreated when applicable.")
                st.rerun()
            else:
                st.warning("Could not mark task complete.")
    else:
        st.info("No pending tasks for this pet.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Generate Schedule")
st.caption("Organize and view all tasks for your pet.")

if st.button("Generate schedule"):
    sorted_tasks = scheduler.sort_by_time(include_completed=False)
    pending_tasks = scheduler.filter_tasks(completed=False)
    completed_tasks = scheduler.filter_tasks(completed=True)
    conflict_warnings = scheduler.detect_time_conflicts(include_completed=False)

    if sorted_tasks:
        st.success("Schedule generated!")
        st.markdown(f"**{scheduler.owner.name}'s Schedule for {st.session_state.pet.name}**")

        if conflict_warnings:
            for warning in conflict_warnings:
                st.warning(warning)
        else:
            st.success("No time conflicts detected.")

        sorted_data = [
            {
                "Description": task.description,
                "Time": task.time,
                "Frequency": task.frequency,
                "Status": "✓ Completed" if task.completed else "Pending",
            }
            for task in sorted_tasks
        ]
        st.markdown("#### Sorted Schedule")
        st.table(sorted_data)

        st.markdown("#### Pending Tasks")
        st.table(
            [
                {"Description": task.description, "Time": task.time, "Frequency": task.frequency}
                for task in pending_tasks
            ]
        )

        st.markdown("#### Completed Tasks")
        if completed_tasks:
            st.table(
                [
                    {"Description": task.description, "Time": task.time, "Frequency": task.frequency}
                    for task in completed_tasks
                ]
            )
        else:
            st.info("No completed tasks yet.")
    else:
        st.info("No tasks to schedule. Add tasks above first.")
