# Database Context

## Database
- Engine: none. Users are stored in `data/users.json` (a JSON list).
- Schema(s): one record type `{ "empid": str, "username": str, "designation": str }`.
- Tenant strategy: single tenant.

## Tables / Views
None. Adding a database is an architecture change (see `architecture.md`).

## Rules
- Never invent columns or relationships.
- Never change schema without explicit approval.
- Tenant-scoped reads/writes must be verified.
