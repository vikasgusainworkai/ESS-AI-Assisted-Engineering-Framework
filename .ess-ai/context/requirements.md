# Requirements

## Requirement
Maintain the HR employee list: list, add (+), edit and delete employees by EMPID. Bugs arrive as tickets on the ESS Tracker board (ESS-201, ESS-202, ESS-203); each ticket has acceptance criteria that are the requirement for that fix.

## Acceptance Criteria
- See the ticket (`python tools/tracker.py show <ID>`).

## Out of Scope
- Authentication, roles, databases, new UI screens.

## Business Rules
- EMPID is the unique key and matches exactly.
- All three fields are required; surrounding spaces are trimmed.

## Affected Users / Tenants
- HR Team (single tenant).

## Evidence / References
- `jira_lite/seed_tickets.json`, `tests/test_user_service.py`
