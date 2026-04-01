# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Features

- Sorting by time: Tasks are sorted chronologically using `Scheduler.sort_by_time()` with a key that parses `HH:MM` into `(hour, minute)` tuples.
- Multi-factor organization: `Scheduler.organize_tasks()` sorts by completion status, frequency order (`daily`, `weekly`, `monthly`, `as needed`), time, then description.
- Filtering by status and pet: `Scheduler.filter_tasks()` supports filtering by completion state and optional pet name.
- Conflict warnings (non-crashing): `Scheduler.detect_time_conflicts()` detects duplicate times and returns warning messages instead of raising exceptions.
- Daily/weekly recurrence: `Scheduler.mark_task_completed()` marks the current task complete and automatically creates a new incomplete instance for recurring tasks.
- Pending-only retrieval: `Scheduler.get_pending_tasks()` returns incomplete tasks for focused action lists.
- Grouped schedule views: `Scheduler.get_tasks_grouped_by_pet()` returns tasks grouped by pet name.

## Demo

<a href="/demo/image.png" target=_blank><img src="/demo/image.png" title='PawPal App' width='' alt='PawPal App' class='center-block'></a>
<a href="/demo/image copy.png" target=_blank><img src="/demo/image copy.png" title='PawPal App' width='' alt='PawPal App' class='center-block'></a>
