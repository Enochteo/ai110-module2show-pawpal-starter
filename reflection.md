# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial UML used five main classes: `Owner`, `Pet`, `Task`, `ScheduleItem`, and `Scheduler`.
- `Owner` stored name, available minutes for the day, and preference flags (for example, avoid late-evening walks).
- `Pet` stored pet profile data like species and routine notes.
- `Task` represented a care activity with a title, duration, priority, optional time window, and optional recurrence.
- `ScheduleItem` represented a task that was placed in a specific start/end time slot.
- `Scheduler` took owner/pet/task data, applied constraints, and produced both the final daily plan and an explanation string for each scheduled task.

**b. Design changes**

- Yes. I originally put ranking logic directly inside the `Task` class, but I moved it into `Scheduler`.
- That change made the design cleaner because `Task` became a plain data model, while scheduling decisions stayed centralized in one place.
- I also added a separate explanation step after scheduling so the app can show why a task was selected or skipped.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers total time available, task duration, priority (`high`, `medium`, `low`), and owner preferences (such as preferred windows for walk or feeding tasks).
- I treated hard constraints first (cannot exceed available minutes, must respect strict time windows), then optimized soft constraints (preference matching).
- Priority mattered most because missing high-priority items like medication is more harmful than deferring lower-priority enrichment tasks.

**b. Tradeoffs**

- One clear tradeoff is that the scheduler may skip some low-priority tasks if the day is overbooked.
- This is reasonable because the goal is a realistic daily plan, not a perfect all-inclusive plan. In real life, a feasible schedule that consistently covers critical care is better than an overloaded schedule that is likely to fail.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI for UML brainstorming, naming/class responsibility checks, and debugging edge-case behavior in scheduling.
- The most helpful prompts were specific and constraint-based, for example: "Given 90 minutes total and these tasks, what scheduling order minimizes risk if everything does not fit?" and "Refactor this method to separate scoring from formatting explanation output."

**b. Judgment and verification**

- One AI suggestion used a purely duration-based greedy sort, which would sometimes place shorter low-priority tasks before high-priority medication tasks.
- I rejected that as-is, wrote a quick test scenario, and compared outcomes. The test showed a behavioral regression, so I switched to a weighted priority-first approach with time-window checks.

---

## 4. Testing and Verification

**a. What you tested**

- I tested: priority ordering, behavior when total task time exceeds availability, enforcement of strict time windows, and deterministic output for the same input.
- These tests are important because they validate both correctness (critical tasks are not accidentally dropped) and trust (users get predictable plans).

**b. Confidence**

- I am moderately high confidence in the core behavior for normal daily inputs and common conflicts.
- Next edge cases I would test are tied priorities with different durations, zero/invalid durations from user input, overlapping hard windows, and multi-pet scenarios sharing one owner's time budget.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with separating data models from scheduling policy. That made the code easier to reason about and easier to connect to the Streamlit UI.

**b. What you would improve**

- In another iteration, I would add lightweight optimization (for example, scoring plus backtracking for near-tie decisions) and stronger explainability so each skipped task includes a clear reason code.
- I would also improve the UI to allow editing/deleting tasks and showing "what changed" when constraints are updated.

**c. Key takeaway**

- My biggest takeaway is that AI is best used as a fast design and debugging partner, but final decisions still need explicit constraints, tests, and human judgment.
