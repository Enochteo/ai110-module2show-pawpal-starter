from pawpal_system import Pet, Task


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
