# ESS Claude Code demo: User Management app

Fix real bug tickets by typing prompts in **Claude Code in VS Code**. The ESS starter kit inside this project makes every fix follow the framework, and commits and pushes it for you after you approve.

```
Ticket on the board -> prompt: plan (Claude stops) -> you approve
  -> Claude writes a failing test   (ESS auto-test hook: RED)
  -> Claude fixes the code          (ESS auto-test hook: GREEN)
  -> Claude shows the diff (stops)  -> you say "Approved, commit and push it"
  -> permission prompt (the approval gate) -> tools/ess_ship.py:
       guardrail check + tests -> branch fix/ESS-201-... -> commit -> push to origin
  -> the ticket moves to In Review with the diff -> a human approves on the board
```

**Start here: [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md)**: setup, then exactly what to type in the terminal and in Claude Code at every step.

Needs Python 3.10+ (3.12 recommended), Git and Claude Code. Nothing to `pip install`.

## Quick start (Windows PowerShell, in this folder)

```
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python reset_demo.py              # git repo, baseline, a local "company server" remote, tickets
python jira_lite\server.py        # terminal 2: ticket board  http://127.0.0.1:5055
python app\server.py              # terminal 3: the app       http://127.0.0.1:5070
claude                            # terminal 4: Claude Code (trust the folder)
```

Then in Claude Code: `Fix ticket ESS-201. Start it on the board, read the ticket and the code, run the tests, then tell me the root cause and your plan. Do not change any file yet.`

## The bugs on the board

| Ticket | What a user sees | Where |
|---|---|---|
| **ESS-201** | Delete EMP1 and EMP10, EMP11 disappear too (delete matches by prefix) | `delete_user()` |
| **ESS-202** | Add EMP2 again and a second EMP2 row appears | `add_user()` |
| **ESS-203** | A username of only spaces is saved; extra spaces are kept | `_validate()` |

You can also create your own ticket with **+ New ticket** on the board and ask Claude to fix it.

## What makes it work (all from the ESS starter kit)

| File | Role |
|---|---|
| `CLAUDE.md`, `AGENTS.md` | The ESS rules and this project's ticket workflow; Claude Code loads them automatically |
| `.claude/settings.json` | Hooks: prompt guard, action guard, **auto-test after every edit**. Permissions: tests and ticket commands allowed; **the ship command always asks**; `git commit` / `git push` denied for the AI |
| `tools/ess_autotest.py` | Runs the tests after each AI edit and shows GREEN or RED in the chat |
| `tools/ess_ship.py` | The only way to commit: guardrail check + tests, branch, commit of the named files, push, ticket update |
| `tools/ess_guard.py` | The guardrails (blocked prompts, protected files, Definition of Tested) |
| `.ess-ai/` | Rules, prompts, checklists and this project's context (filled in) |
| `.ess-ai/automation.json` | Auto-test command, remote, PR setting, and `after_ship` (moves the ticket on the board) |
| `.claude/commands/` | `/ess-fix`, `/ess-ship`, `/ess-check`, `/ess-bootstrap` and the rest of the ESS prompt library |
| `tools/tracker.py` | Ticket commands for the board (list, show, start, comment). Stand-in for your Jira / Azure DevOps connector |
| `reset_demo.py` | Back to the start: buggy code, users, tickets, branches, a fresh local remote (`--remote <url>` to use GitHub) |
| `jira_lite/`, `app/`, `data/` | The ticket board and the User Management app |

The app reloads `app/user_service.py` when it changes, so after a fix just refresh the browser. It uses port 5070 because browsers block 5060.
