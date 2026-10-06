# Claude Code — ESS demo: User Management app

@AGENTS.md

## This project
- `app/user_service.py` is the business logic (EMPID, username, designation). `app/server.py` serves it at http://127.0.0.1:5070 and reloads the code when the file changes, so a fix is visible after a browser refresh.
- Tests are `unittest` in `tests/`. Run them with `python -m unittest discover -s tests -t . -v`. Name a ticket's regression test file `tests/test_ess_<number>.py` (for ESS-201: `tests/test_ess_201.py`).
- Tickets live on the ESS Tracker board at http://127.0.0.1:5055. Use `python tools/tracker.py` for every ticket action: `list`, `show <ID>`, `start <ID>`, `comment <ID> "text"`. Never edit `jira_lite/` or `data/`.
- Only `app/` and `tests/` may change for a ticket. Everything else is protected (`.ess-ai/guardrails.json`).

## Demo mode: keep it short (this is a live demo)
- Do not read every rule or context file. Read only: the ticket, `app/user_service.py`, the existing tests.
- Every reply is at most 8 lines: no tables, no long explanations, no extra options.
- Combine commands into one Bash call where possible. Do not re-run tests the auto-test hook already ran.

## Ticket workflow (3 prompts from the developer)
1. **Plan.** `python tools/tracker.py start <ID>` then `show <ID>`; read the code; run the tests once. Reply in max 6 lines: root cause (file:line), the one-line fix, the test you will add. Post the same in one line with `python tools/tracker.py comment`. **STOP. No edits before approval.**
2. **On "approved": test, then fix, in one go.** Write `tests/test_ess_<number>.py` (2-3 small tests); the auto-test hook shows RED. Then make the smallest fix in `app/`; the hook shows GREEN. Show `git diff --stat` and the changed lines only. Reply: "RED -> GREEN (N passed). Approve commit and push?" **STOP.**
3. **On "commit and push":** run once (the developer gets a permission prompt):
   `python tools/ess_ship.py --ticket <ID> --title "<summary>" --body "<one sentence>" --files <changed files>`
   Reply in 2 lines: branch, commit, pushed, ticket In Review.

Never run `git commit`, `git push`, `git checkout main` or `git reset` yourself; they are denied. If ship STOPS, quote the reason in one line.
