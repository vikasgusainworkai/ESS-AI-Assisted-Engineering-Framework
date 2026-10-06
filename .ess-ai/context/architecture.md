# Approved Architecture

## System Boundary
- `app/static/index.html`: the UI (table, + Add, Edit, Delete).
- `app/server.py`: standard-library HTTP server and REST API on port 5070. Reloads `app/user_service.py` when it changes.
- `app/user_service.py`: all business rules and validation. Persists to `data/users.json`.
- `jira_lite/`: the ticket board (a stand-in for Jira). Not part of the product.

## Allowed Extension Points
- Business rules and validation in `app/user_service.py`.
- Tests in `tests/`.

## Protected Decisions
- No database, no ORM, no new third-party packages (standard library only).
- No authentication in this demo app (out of scope).
- Data files, the ticket board, tools and the ESS control plane are protected (`.ess-ai/guardrails.json`).

## ADRs
- ADR-001: JSON file storage, standard library only, so the demo runs anywhere with Python and git.

## Architecture Change Rule
AI may propose architecture changes, but must not implement material architecture, database, authentication or infrastructure changes without explicit approval.
