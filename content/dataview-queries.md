# Dataview Queries

Useful queries you can embed in any note. Requires the Dataview plugin.

## This Week's Schedule (static overview)

Use this in a dashboard note:

```dataview
TABLE workout as "Workout", completed as "Done", duration_min as "Minutes"
FROM ""
WHERE type = "strength" AND date >= date(today) - dur(7 days)
SORT date ASC
```

## Completed Workouts (last 30 days)

```dataview
TABLE date as "Date", workout as "Workout", duration_min as "Min"
FROM ""
WHERE completed = true AND date >= date(today) - dur(30 days)
SORT date DESC
```

## Streak Counter

```dataview
LIST
FROM ""
WHERE completed = true
SORT date DESC
LIMIT 10
```

## Full Calendar Setup

If you have the **Full Calendar** plugin installed:

1. Go to Settings → Full Calendar
2. Under "Calendars," add a new calendar of type **Daily Note**
3. Set the folder to wherever you store your daily workout logs
4. Set the date format to match your frontmatter `date` field (e.g., `YYYY-MM-DD`)

This will render your completed/planned workouts on a calendar view.

## Alternative: Calendar Plugin with Frontmatter

The **Calendar** plugin (by Liam Cain) + **Dataview** gives you a sidebar calendar. Clicking a day shows/creates the daily note for that date. Combined with the template above, it creates a natural "click day → log workout" flow.

## Weekly View with Dataview

Paste this in any note for a week-at-a-glance:

```dataview
TABLE WITHOUT ID
  dateformat(date, "EEE") as "Day",
  workout as "Workout",
  choice(completed, "✓", "—") as "Status"
FROM ""
WHERE type = "strength" AND date >= date(today) - dur(7 days)
SORT date ASC
```
