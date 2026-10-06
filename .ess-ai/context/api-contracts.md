# API Contracts

| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/api/users` | - | 200, list of `{empid, username, designation}` | - |
| POST | `/api/users` | `{empid, username, designation}` | 201, the new user | 400 `{error}` on validation (ValueError) |
| PUT | `/api/users/<empid>` | `{username, designation}` | 200, the updated user | 404 unknown EMPID (KeyError), 400 validation |
| DELETE | `/api/users/<empid>` | - | 200, the deleted user | 404 unknown EMPID (KeyError) |

`UserService` raises `ValueError` for invalid input and `KeyError` for an unknown EMPID; the server maps them to 400 and 404.

AI must not silently change an existing contract.
