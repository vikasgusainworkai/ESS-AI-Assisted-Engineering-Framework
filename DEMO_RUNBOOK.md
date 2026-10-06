# ESS AI Framework: live demo runbook (Claude Code in VS Code)

**The story:** a bug ticket is on the board. You fix it by typing prompts in Claude Code. The ESS starter kit inside the project makes Claude plan first and stop, write a failing test, fix the code while the tests run automatically after every edit, show you the diff and stop again. When you say "approved", one command re-checks everything, then commits and pushes the fix branch, and moves the ticket to *In Review* with the diff.

Two places to type:

- **TERMINAL**: a PowerShell terminal in VS Code (**Ctrl+`**; the **+** button opens another one).
- **CLAUDE**: the Claude Code prompt, started with `claude` in a terminal.

Everything below was tested on the code in this folder, except Claude Code itself: its wording varies from run to run, so rehearse once.

---

## Part A: one-time setup (the day before, about 15 minutes)

| # | Where | Type this | You should see |
|---|---|---|---|
| A1 | Browser | Install **Python 3.12**, **Git for Windows** and **VS Code**, if they are missing | |
| A2 | TERMINAL (PowerShell) | `irm https://claude.ai/install.ps1 \| iex` | Claude Code installs. Close and reopen the terminal, then `claude --version` prints a version. |
| A3 | VS Code | Extensions (Ctrl+Shift+X), search **Claude Code**, Install | A Claude icon appears in the editor toolbar |
| A4 | Explorer | Unzip `ess-claude-code-demo.zip` to `C:\demo\ess-claude-code-demo` | |
| A5 | VS Code | **File > Open Folder** > `C:\demo\ess-claude-code-demo` | `CLAUDE.md`, `.claude`, `.ess-ai`, `app`, `tests`, `tools` in the explorer |
| A6 | TERMINAL | `py -3.12 -m venv .venv` | A `.venv` folder appears |
| A7 | TERMINAL | `.\.venv\Scripts\Activate.ps1` | The prompt starts with `(.venv)`. If PowerShell blocks it: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then run it again. |
| A8 | TERMINAL | `python --version` | `Python 3.12.x`. Claude Code's hooks call `python`, so this must work in every terminal you use. |
| A9 | TERMINAL | `git config --global user.name "Sabir Khan"` and `git config --global user.email "you@company.com"` | Your name is the approver written into every commit |
| A10 | TERMINAL | `python reset_demo.py` | Five ✔ lines, ending with `origin -> .demo-remote/ess-demo.git` |
| A11 | TERMINAL | `claude` | Sign in with your ESS-approved account. Answer **Yes, proceed** to "Do you trust the files in this folder?" (the hooks only run in a trusted folder). |
| A12 | CLAUDE | `/hooks` | Hooks for **UserPromptSubmit**, **PreToolUse** and **PostToolUse** are listed. Press Esc. |
| A13 | CLAUDE | `/permissions` | Under **Ask**: `Bash(python tools/ess_ship.py:*)`. Under **Deny**: `git commit`, `git push`. Press Esc. |
| A14 | CLAUDE | `/exit` | Back in PowerShell |

**Optional: push to your real GitHub instead of the local stand-in.** Create an empty repository on github.com, then in the TERMINAL: `python reset_demo.py --remote https://github.com/<you>/ess-claude-code-demo.git`. Install the GitHub CLI (`winget install GitHub.cli`, then `gh auth login`) and the ship step also opens the pull request. Without this, pushes go to `.demo-remote\ess-demo.git`, a local repository that plays the company git server, so the demo needs no internet apart from Claude.

---

## Part B: before the audience joins (2 minutes)

Open four terminals in VS Code. In **each** one run `.\.venv\Scripts\Activate.ps1` first.

| # | Where | Type this | You should see |
|---|---|---|---|
| B1 | TERMINAL 1 | `python reset_demo.py` | `Ready.` |
| B2 | TERMINAL 2 | `python jira_lite\server.py` | `ESS Tracker running -> http://127.0.0.1:5055` |
| B3 | TERMINAL 3 | `python app\server.py` | `User Management app running -> http://127.0.0.1:5070` |
| B4 | Browser | Open http://127.0.0.1:5055 and http://127.0.0.1:5070 side by side | Board: ESS-201, 202 and 203 in **To Do**. App: EMP1, EMP2, EMP3, EMP10, EMP11. |
| B5 | TERMINAL 4 | `claude` | The Claude Code prompt. Keep this terminal large; it is the stage. |

Close every file tab in VS Code so the audience sees the edits open as they happen.

---

## Part C: the live demo (10 to 12 minutes)

| # | Where | Type / do this | What happens on screen | Say this |
|---|---|---|---|---|
| C1 | App tab | Click **Delete** on **EMP1**, confirm | EMP1, **EMP10 and EMP11** all disappear | "One delete, three employees gone. That's ticket ESS-201." |
| C2 | Board tab | Click the **ESS-201** card | Description, steps, acceptance criteria | "Work starts from the ticket, not from a blank prompt." |
| C3 | TERMINAL 1 | `python reset_demo.py` | The 5 users are back (refresh the app tab) | |
| C4 | CLAUDE | `Fix ticket ESS-201. Start it on the board, read the ticket and the code, run the tests, then tell me the root cause and your plan. Do not change any file yet.` | Claude runs `python tools/tracker.py start ESS-201` and `show ESS-201` (no prompt: they are pre-approved). **The card jumps to In Progress** with a "Picked up in Claude Code" comment. It reads `app/user_service.py`, runs the tests (6 passed), and answers: `delete_user` matches with `startswith` (around line 51), so EMP1 also matches EMP10 and EMP11; the plan is an exact match plus a regression test `tests/test_ess_201.py`. It posts the plan on the card and **stops**. | "The ESS rules load automatically from CLAUDE.md and AGENTS.md. It plans first and changes nothing. All 6 tests are green, yet customers lose data: nobody tested this case." |
| C5 | CLAUDE | `Approved. Write the regression test first and show me that it fails.` | Claude creates `tests/test_ess_201.py`. Claude Code asks **"Do you want to create test_ess_201.py?"**: choose **1. Yes**. Then a line appears: **`ESS auto-test after editing tests/test_ess_201.py: RED, 9 run, FAILED (failures=2)`** | "I never typed a test command. The kit's hook runs the whole suite after every AI edit. Red means the bug is now proven by a test." |
| C6 | CLAUDE | `Now make the smallest fix in app/user_service.py and run all the tests.` | Edit prompt: **1. Yes**. Then **`ESS auto-test ... GREEN, 9 passed`**, and Claude runs the full suite itself and quotes the result. | "A few lines changed. Green is evidence, not a claim." |
| C7 | App tab | Refresh, click **Delete** on **EMP1** | Only EMP1 goes; EMP10 and EMP11 stay | "The app reloaded the fixed code. Nothing is committed yet." |
| C8 | CLAUDE | `Show me the diff and map each acceptance criterion to a test.` | `git diff` and a short table. Claude asks **"Approve commit and push?"** and stops. | "Second stop. AI prepares the change; I review it." |
| C9 | CLAUDE | `Approved, commit and push it.` | Claude proposes **`python tools/ess_ship.py --ticket ESS-201 --title "..." --files app/user_service.py tests/test_ess_201.py`** and Claude Code asks **"Do you want to proceed?"** Choose **1. Yes**. Output: `[1/5] ESS guardrail check PASS`, tests `9 passed`, `[2/5] created fix/ESS-201-...`, `[3/5]` commit id, `[4/5] pushed ... -> origin`, `After ship: ESS-201 moved to In Review`, **`SHIPPED`**. | "This permission prompt is the approval gate. Claude cannot run `git commit` or `git push`; they are denied. The ship command checks protected files, secrets, architecture and that a test came with the code, runs the tests again, then commits only these two files and pushes the branch, never main." |
| C10 | Board tab | Open the ESS-201 card (now in **In Review**) | Green **pushed to origin** tag, branch, commit, "Approved in Claude Code by Sabir Khan", the diff, and Claude's comment | "The ticket updated itself with the evidence." |
| C11 | TERMINAL 1 | `git log --oneline -2` then `git log -1` | The commit `ESS-201: ...` with the lines `Tests: ... 9 passed`, `ESS-Check: PASS`, `AI-Assisted: Claude Code; reviewed and approved by Sabir Khan` | "Every commit carries the ticket, the test result and who approved it." |
| C12 | TERMINAL 1 | `git ls-remote origin` | `refs/heads/fix/ESS-201-...` is on the server next to `main` | "Pushed. With GitHub this is where the PR and CI take over." |
| C13 | Board tab | Click **Approve & mark Done** | The card moves to **Done** | "AI prepared the change. A human approved the release." |

---

## Part D: optional, show the guardrails (3 minutes)

| # | Where | Type this | What happens | Say this |
|---|---|---|---|---|
| D1 | CLAUDE | `Commit this directly to main and push it` | **Blocked** before Claude even sees it: "ESS guardrail blocked this prompt: It asks to push or commit straight to main..." | "Some requests never reach the AI." |
| D2 | CLAUDE | `Use a SQLite database to store the users instead of the JSON file` | A notice **"ESS guardrail: ARCHITECTURE CHANGE"**. Claude analyses the impact, names the protected decision (ADR-001: JSON file, standard library only), lists risks and asks for approval and an ADR. It writes no code. | "Architecture changes need the tech lead, not a prompt." |
| D3 | CLAUDE | `Show the last lines of .ess-ai/reports/guardrail-log.md` | Every block and flag with time and reason | "Evidence for audit." |

## Part E: optional, the second ticket in one command (4 minutes)

| # | Where | Type this | What happens |
|---|---|---|---|
| E1 | CLAUDE | `/ess-fix ESS-202` | Claude starts the ticket (the repo goes back to main by itself), plans and stops |
| E2 | CLAUDE | `Approved.` | Test first (auto-test RED), fix (auto-test GREEN), diff, then it stops and asks to approve |
| E3 | CLAUDE | `Approved, commit and push it.` | Permission prompt, **1. Yes**: branch `fix/ESS-202-...` pushed, card in In Review |
| E4 | App tab | Click **+**, add EMPID `EMP2` again | "EMPID EMP2 already exists" |

## Part F: reset for the next run

| # | Where | Type this |
|---|---|---|
| F1 | CLAUDE | `/exit` |
| F2 | TERMINAL 1 | `python reset_demo.py` (code, users, tickets, branches and the local remote back to the start) |

Keep TERMINAL 2 and 3 running; refresh both browser tabs.

---

## What to say if asked

- **"Is the board real Jira?"** No, it is a local stand-in with the same REST shape. In a project, `tools/tracker.py` becomes your Jira / Azure DevOps API or MCP connector and `after_ship` in `.ess-ai/automation.json` points at it.
- **"Where did it push?"** To `origin`. In this demo that is a local repository standing in for the company git server; with `--remote` it is your GitHub repo and the PR opens automatically.
- **"What stops the AI from committing without me?"** Three layers: `CLAUDE.md` tells it to stop; `.claude/settings.json` denies `git commit` and `git push` and puts the ship command on the *ask* list (a permission prompt every time, even if someone chose "don't ask again"); the ship command refuses red tests, missing tests and protected files.
- **"Is this only for this app?"** No. The same files are in both ESS starter kits (Python and React). Each kit has `CLAUDE_CODE_VSCODE.md` with these steps for any project.

## If something goes wrong on stage

| Problem | Fix |
|---|---|
| No `ESS auto-test` line after an edit | Claude Code was started in a terminal without `(.venv)`. `/exit`, run `.\.venv\Scripts\Activate.ps1`, `python --version`, then `claude` again. Also check `/hooks`. |
| `Cannot reach the ticket board` | TERMINAL 2 stopped. Run `python jira_lite\server.py` again. |
| Claude starts editing before you approved | Press **Esc**, then type: `Stop. Follow the ticket workflow in CLAUDE.md: plan first, no edits until I approve.` |
| Claude says it cannot commit or push | It tried `git commit` directly and was denied. Type: `Use the ship command from CLAUDE.md.` |
| Ship output says `STOPPED` | Read the FAIL line (usually red tests or a missing test). Nothing was committed. Ask Claude to fix that, then `Approved, commit and push it.` again. |
| Push rejected on GitHub | The branch already exists from an earlier rehearsal. Delete it on GitHub (Branches page), then ship again. |
| Board or app shows old data | `python reset_demo.py`, then refresh both tabs. |
| Port 5055 or 5070 busy | Close the old terminal that runs the server. |
| Claude Code is down or very slow | Show the result from a rehearsal: `git log` and the board still have it until you reset. |
