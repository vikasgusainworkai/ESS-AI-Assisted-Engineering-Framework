# Claude Code — ESS demo: User Management app

@AGENTS.md

## This project
- `app/user_service.py` is the business logic (EMPID, username, designation). `app/server.py` serves it at http://127.0.0.1:5070 and reloads the code when the file changes, so a fix is visible after a browser refresh.
- Tests are `unittest` in `tests/`. Run them with `python -m unittest discover -s tests -t . -v`. Name a ticket's regression test file `tests/test_ess_<number>.py` (for ESS-201: `tests/test_ess_201.py`).
- Tickets live on the ESS Tracker board at http://127.0.0.1:5055. Use `python tools/tracker.py` for every ticket action: `list`, `show <ID>`, `start <ID>`, `comment <ID> "text"`. Never edit `jira_lite/` or `data/`.
- Only `app/` and `tests/` may change for a ticket. Everything else is protected (`.ess-ai/guardrails.json`).

## Ticket workflow (follow it for every bug, whether the developer types /ess-fix or plain prompts)
1. `python tools/tracker.py start <ID>` (card to In Progress, repo on a clean main), then `python tools/tracker.py show <ID>`.
2. Read the code and the existing tests, run the tests once (baseline). Explain why the existing tests did not catch the bug.
3. Reply with the root cause (file:line), the smallest fix, the regression test you will add, files to change, risks and UNKNOWNs. Post a 2 to 3 line summary of the plan on the card with `python tools/tracker.py comment`. **STOP and wait for approval. Do not edit files before the developer approves.**
4. After approval: write the regression test first. The ESS auto-test hook runs the suite after every edit; show that the new test fails (red) for the reason in the ticket.
5. Make the smallest fix in `app/`. The auto-test must be green; also run the full test command and quote the result.
6. Show `git diff`, one line per change, and map each acceptance criterion to a test. Ask "Approve commit and push?" **STOP.**
7. When the developer approves, ship it (one command, the developer gets a permission prompt):
   `python tools/ess_ship.py --ticket <ID> --title "<summary>" --type fix --body "<root cause and fix>" --files <changed files>`
   It re-runs the guardrail check and the tests, creates `fix/<ID>-<summary>`, commits only those files, pushes the branch to `origin` and moves the card to In Review with the diff.
8. Report branch, commit, tests and push result in two or three lines.

Never run `git commit`, `git push`, `git checkout main` or `git reset` yourself; they are denied. If the ship command STOPS, quote the reason and fix only what is inside the approved scope.
