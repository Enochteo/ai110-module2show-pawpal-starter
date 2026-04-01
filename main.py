from pawpal_system import Owner, Pet, Scheduler, Task


def seed_sample_data() -> Owner:
    owner = Owner(name="Jordan", available_minutes=120)

    dog = Pet(name="Mochi", species="dog", age_years=3, routine_notes="Needs two walks")
    cat = Pet(name="Luna", species="cat", age_years=5, routine_notes="Prefers evening play")

    # Add tasks OUT OF ORDER to test sorting
    dog.add_task(Task(description="Dinner feeding", time="18:00", frequency="daily"))
    cat.add_task(Task(description="Laser play", time="20:00", frequency="daily"))
    dog.add_task(Task(description="Morning walk", time="07:30", frequency="daily"))
    dog.add_task(Task(description="Training session", time="09:00", frequency="weekly"))
    cat.add_task(Task(description="Medication", time="09:00", frequency="daily"))
    cat.add_task(Task(description="Wet food", time="12:00", frequency="daily"))
    dog.add_task(Task(description="Afternoon walk", time="14:00", frequency="daily"))
    cat.add_task(Task(description="Bedtime cuddles", time="22:00", frequency="daily"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    return owner


def print_todays_schedule(owner: Owner) -> None:
    scheduler = Scheduler(owner)
    tasks = scheduler.organize_tasks(include_completed=False)

    print("Today's Schedule")
    print("-" * 40)

    if not tasks:
        print("No tasks scheduled.")
        return

    for task in tasks:
        print(f"{task.time} | {task.description} ({task.frequency})")


def print_sorted_by_time_demo(owner: Owner) -> None:
    """Demonstrate the sort_by_time() method."""
    scheduler = Scheduler(owner)
    tasks = scheduler.sort_by_time(include_completed=False)

    print("\n📋 Tasks Sorted by Time (Chronological Order)")
    print("-" * 50)
    
    for task in tasks:
        print(f"{task.time} | {task.description}")


def print_filter_by_completion_demo(owner: Owner) -> None:
    """Demonstrate filter_tasks() by completion status."""
    scheduler = Scheduler(owner)
    
    print("\n✅ Filter: Completed Tasks")
    print("-" * 50)
    completed_tasks = scheduler.filter_tasks(completed=True)
    if completed_tasks:
        for task in completed_tasks:
            print(f"  {task.description}")
    else:
        print("  No completed tasks yet.")
    
    print("\n⏳ Filter: Incomplete Tasks")
    print("-" * 50)
    incomplete_tasks = scheduler.filter_tasks(completed=False)
    for task in incomplete_tasks:
        print(f"  {task.description}")


def print_filter_by_pet_demo(owner: Owner) -> None:
    """Demonstrate filter_tasks() by pet name."""
    scheduler = Scheduler(owner)
    
    print("\n🐕 Tasks for Mochi (Dog)")
    print("-" * 50)
    mochi_tasks = scheduler.filter_tasks(pet_name="Mochi")
    for task in mochi_tasks:
        print(f"  {task.time} | {task.description}")
    
    print("\n🐱 Tasks for Luna (Cat)")
    print("-" * 50)
    luna_tasks = scheduler.filter_tasks(pet_name="Luna")
    for task in luna_tasks:
        print(f"  {task.time} | {task.description}")


def print_filter_combined_demo(owner: Owner) -> None:
    """Demonstrate filter_tasks() with both criteria."""
    scheduler = Scheduler(owner)
    
    print("\n🐕 Incomplete Tasks for Mochi (Combined Filter)")
    print("-" * 50)
    mochi_incomplete = scheduler.filter_tasks(completed=False, pet_name="Mochi")
    for task in mochi_incomplete:
        print(f"  {task.time} | {task.description}")
    
    # Mark a task as completed for demo
    scheduler.mark_task_completed("Luna", "Laser play")
    
    print("\n🐱 Completed Tasks for Luna (After marking one complete)")
    print("-" * 50)
    luna_completed = scheduler.filter_tasks(completed=True, pet_name="Luna")
    for task in luna_completed:
        print(f"  {task.description}")


def print_recurring_task_demo(owner: Owner) -> None:
    """Demonstrate automatic recurring task creation."""
    scheduler = Scheduler(owner)
    
    print("\n🔄 Recurring Task Demo - Before Completion")
    print("-" * 50)
    mochi_tasks = scheduler.filter_tasks(pet_name="Mochi")
    print(f"Mochi has {len(mochi_tasks)} tasks total")
    for task in mochi_tasks:
        status = "✓" if task.completed else "○"
        print(f"  {status} {task.time} | {task.description} ({task.frequency})")
    
    print("\n🔄 Marking 'Morning walk' as completed...")
    print("-" * 50)
    scheduler.mark_task_completed("Mochi", "Morning walk")
    
    mochi_tasks = scheduler.filter_tasks(pet_name="Mochi")
    print(f"Mochi now has {len(mochi_tasks)} tasks total (new one created!)")
    for task in mochi_tasks:
        status = "✓" if task.completed else "○"
        print(f"  {status} {task.time} | {task.description} ({task.frequency})")
    
    # Count completed vs incomplete
    completed = scheduler.filter_tasks(completed=True, pet_name="Mochi")
    incomplete = scheduler.filter_tasks(completed=False, pet_name="Mochi")
    print(f"\n  Summary: {len(completed)} completed, {len(incomplete)} incomplete")


def print_conflict_detection_demo(owner: Owner) -> None:
    """Demonstrate time conflict detection."""
    scheduler = Scheduler(owner)
    
    print("\n🔔 Conflict Detection Demo - Initial Schedule")
    print("-" * 50)
    
    # Check for conflicts in current schedule (includes intentional same-time tasks)
    all_conflicts = scheduler.detect_time_conflicts()
    if all_conflicts:
        print("Conflicts found:")
        for warning in all_conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts found in current schedule ✓")
    
    # Add another conflicting task intentionally for a second warning
    print("\n🔔 Adding another conflicting task at 20:00...")
    print("-" * 50)
    new_task = Task(
        description="Emergency vet call",
        time="20:00",
        frequency="as needed",
        completed=False
    )
    scheduler.add_task_to_pet("Luna", new_task)
    
    # Check for conflicts again
    conflicts = scheduler.detect_time_conflicts()
    if conflicts:
        print("Conflicts found:")
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts found")
    
    # Check conflicts for a specific pet
    print("\n🔔 Checking conflicts for Luna specifically")
    print("-" * 50)
    luna_conflicts = scheduler.detect_time_conflicts(pet_name="Luna")
    if luna_conflicts:
        for warning in luna_conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts for Luna ✓")
    
    # Show Luna's schedule
    print("\n📋 Luna's full schedule:")
    print("-" * 50)
    luna_tasks = scheduler.filter_tasks(pet_name="Luna")
    for task in sorted(luna_tasks, key=lambda t: t.time):
        print(f"  {task.time} | {task.description}")


def main() -> None:
    owner = seed_sample_data()
    print_todays_schedule(owner)
    print_sorted_by_time_demo(owner)
    print_filter_by_completion_demo(owner)
    print_filter_by_pet_demo(owner)
    print_filter_combined_demo(owner)
    print_recurring_task_demo(owner)
    print_conflict_detection_demo(owner)


if __name__ == "__main__":
    main()
