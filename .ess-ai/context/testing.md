# Testing Context

## Commands
- Unit: `python -m unittest discover -s tests -t . -v`
- Guardrail check: `python tools/ess_guard.py check`
- Auto-test: runs by itself after every Claude edit to `app/` or `tests/` (`tools/ess_autotest.py`).

## Critical Scenarios
- Delete removes exactly one employee (EMPID match is exact, never by prefix).
- An EMPID is unique.
- EMPID, username and designation are required, trimmed, and never blank.
- Data is saved to and reloaded from the JSON file.

## Test Data
`data/seed_users.json`: EMP1, EMP2, EMP3, EMP10, EMP11 (fake names, no personal data). Unit tests use an in-memory `UserService()`.

## Evidence
Every material AI change must report the exact verification performed. A bug fix adds a regression test in `tests/test_ess_<ticket number>.py` that fails before the fix and passes after it.
