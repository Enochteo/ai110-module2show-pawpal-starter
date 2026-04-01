from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Owner:
	name: str
	available_minutes: int
	preferences: dict
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		pass

	def update_preferences(self, new_prefs: dict) -> None:
		pass


@dataclass
class Pet:
	name: str
	species: str
	age_years: int
	routine_notes: str

	def get_care_profile(self) -> dict:
		pass


@dataclass
class Task:
	title: str
	duration_minutes: int
	priority: str
	category: str
	time_window_start: str
	time_window_end: str
	is_required: bool
	recurrence: str

	def fits_window(self, start_time: str) -> bool:
		pass

	def score(self, owner: Owner, pet: Pet) -> float:
		pass


@dataclass
class ScheduleItem:
	task: Task
	start_time: str
	end_time: str
	reason: str

	def overlaps(self, other: ScheduleItem) -> bool:
		pass


@dataclass
class DailySchedule:
	items: list[ScheduleItem] = field(default_factory=list)
	skipped_tasks: list[Task] = field(default_factory=list)
	total_minutes_used: int = 0

	def add_item(self, item: ScheduleItem) -> None:
		pass

	def remaining_minutes(self, owner: Owner) -> int:
		pass

	def explain_plan(self) -> list[str]:
		pass


class Scheduler:
	def rank_tasks(self, tasks: list[Task], owner: Owner, pet: Pet) -> list[Task]:
		pass

	def build_schedule(self, tasks: list[Task], owner: Owner, pet: Pet) -> DailySchedule:
		pass

	def explain_skips(self, skipped: list[Task]) -> list[str]:
		pass
