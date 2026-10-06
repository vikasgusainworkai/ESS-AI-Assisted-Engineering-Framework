# ESS Project Context

## Project
- Project name: ESS User Management (demo)
- Product / module: HR employee list: EMPID, username, designation
- Customer / tenant: internal demo, single tenant
- Business owner: HR Team
- Technical owner: ESS Dev Team
- Repository: this folder (`origin` = `.demo-remote/ess-demo.git`, or your GitHub repo)
- Primary technology: Python 3 standard library (http.server, json, unittest)
- Environments: local only (app http://127.0.0.1:5070, ticket board http://127.0.0.1:5055)

## Purpose
HR adds, edits, lists and deletes employees. Tickets for bugs come from the ESS Tracker board.

## Must Not Change
- The REST API in `api-contracts.md` and the user record shape `{empid, username, designation}`.
- Storage stays a JSON file (`data/users.json`); no database.
- `UserService` public methods: `list_users`, `get_user`, `add_user`, `update_user`, `delete_user`.

## Source of Truth
1. Existing source code and tests
2. Approved architecture / ADRs
3. Database schema and API contracts
4. Product documentation
5. External documentation
6. General AI knowledge

If evidence is missing, report `UNKNOWN`; do not guess.
