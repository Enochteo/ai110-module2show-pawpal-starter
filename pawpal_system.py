from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """Represents a single pet-care activity."""

    description: str
    time: str
    frequency: str
    completed: bool = False

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_complete(self) -> None:
        """Alias for mark_completed."""
        self.mark_completed()

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completed = False

    def update_time(self, new_time: str) -> None:
        """Update the scheduled time for this task."""
        self.time = new_time


@dataclass
class Pet:
    """Stores pet details and the tasks assigned to the pet."""

    name: str
    species: str
    age_years: int
    routine_notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, description: str) -> bool:
        """Remove the first task matching the description."""
        for index, task in enumerate(self.tasks):
            if task.description == description:
                del self.tasks[index]
                return True
        return False

    def get_tasks(self, include_completed: bool = True) -> list[Task]:
        """Return tasks, optionally excluding completed ones."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Owns and manages multiple pets."""

    name: str
    available_minutes: int = 0
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Remove the first pet with the given name."""
        for index, pet in enumerate(self.pets):
            if pet.name == pet_name:
                del self.pets[index]
                return True
        return False

    def get_pet(self, pet_name: str) -> Pet | None:
        """Return the pet with the given name, if present."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self, include_completed: bool = True) -> list[Task]:
        """Collect tasks from all pets owned by this owner."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks(include_completed=include_completed))
        return all_tasks


class Scheduler:
    """Retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        """Initialize a scheduler for a specific owner."""
        self.owner = owner

    def get_all_tasks(self, include_completed: bool = False) -> list[Task]:
        """Return all tasks across the owner's pets."""
        return self.owner.get_all_tasks(include_completed=include_completed)

    def get_tasks_grouped_by_pet(self, include_completed: bool = False) -> dict[str, list[Task]]:
        """Return tasks grouped by pet name."""
        grouped: dict[str, list[Task]] = {}
        for pet in self.owner.pets:
            grouped[pet.name] = pet.get_tasks(include_completed=include_completed)
        return grouped

    def get_pending_tasks(self) -> list[Task]:
        """Return only tasks that are not completed."""
        return self.get_all_tasks(include_completed=False)

    def organize_tasks(self, include_completed: bool = False) -> list[Task]:
        """Return tasks sorted by completion, frequency, time, and description."""
        frequency_order = {
            "daily": 0,
            "weekly": 1,
            "monthly": 2,
            "as needed": 3,
        }

        tasks = self.get_all_tasks(include_completed=include_completed)
        return sorted(
            tasks,
            key=lambda task: (
                task.completed,
                frequency_order.get(task.frequency.strip().lower(), 99),
                task.time,
                task.description.lower(),
            ),
        )

    def mark_task_completed(self, pet_name: str, description: str) -> bool:
        """Mark a matching task as completed for the specified pet."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return False

        for task in pet.tasks:
            if task.description == description:
                task.mark_completed()
                return True

        return False

    def add_task_to_pet(self, pet_name: str, task: Task) -> bool:
        """Add a task to the specified pet if it exists."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return False

        pet.add_task(task)
        return True

    def remove_task_from_pet(self, pet_name: str, description: str) -> bool:
        """Remove a matching task from the specified pet."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return False

        return pet.remove_task(description)
