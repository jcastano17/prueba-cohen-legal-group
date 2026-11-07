# Leg-day visual guide

Two vertical, phone-friendly infographics for the agreed leg-day routine:

- `1-leg-strength.png`: session overview, warm-up, the 5 primary lifts (start → finish) with sets, reps, rest and their active-recovery move.
- `2-calves-ankles.png`: the 3 calf/ankle exercises, then cardio and cool-down.

The routine lives in one place (`source/build.py`) and is checked against the agreed plan on every build. A drawing fix therefore can't change an exercise, set, rep, rest time or recovery move. To rebuild:

```
python3 source/build.py && node source/render.js
```
