from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_marks_status_true() -> None:
    task = Task(description="Feed breakfast", time="08:00", frequency="daily")

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_to_pet_increases_task_count() -> None:
    pet = Pet(name="Mochi", species="dog", age_years=3)
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Evening walk", time="18:30", frequency="daily"))

    assert len(pet.tasks) == initial_count + 1


def test_scheduler_sort_by_time_returns_chronological_order() -> None:
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog", age_years=3)

    mochi.add_task(Task(description="Dinner", time="18:00", frequency="daily"))
    mochi.add_task(Task(description="Morning walk", time="07:30", frequency="daily"))
    mochi.add_task(Task(description="Lunch", time="12:00", frequency="daily"))

    owner.add_pet(mochi)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time(include_completed=False)

    assert [task.time for task in sorted_tasks] == ["07:30", "12:00", "18:00"]


def test_marking_daily_task_complete_creates_next_occurrence() -> None:
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog", age_years=3)
    mochi.add_task(Task(description="Morning walk", time="07:30", frequency="daily"))

    owner.add_pet(mochi)
    scheduler = Scheduler(owner)

    was_marked = scheduler.mark_task_completed("Mochi", "Morning walk")

    assert was_marked is True
    assert len(mochi.tasks) == 2
    assert sum(task.description == "Morning walk" for task in mochi.tasks) == 2
    assert sum(task.completed for task in mochi.tasks) == 1
    assert sum(not task.completed for task in mochi.tasks) == 1


def test_detect_time_conflicts_flags_duplicate_times() -> None:
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog", age_years=3)
    luna = Pet(name="Luna", species="cat", age_years=5)

    mochi.add_task(Task(description="Training", time="09:00", frequency="weekly"))
    luna.add_task(Task(description="Medication", time="09:00", frequency="daily"))

    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner)

    warnings = scheduler.detect_time_conflicts()

    assert len(warnings) == 1
    assert "09:00" in warnings[0]
    assert "Training" in warnings[0]
    assert "Medication" in warnings[0]
