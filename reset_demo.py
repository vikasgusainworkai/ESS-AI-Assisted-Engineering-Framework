#!/usr/bin/env python3
"""
Reset the demo to its starting state (run this before every demo):
  * restores the buggy app/user_service.py and removes the regression tests Claude wrote
  * resets the user list (data/users.json) and the tickets (ESS-201..203 back in 'To Do')
  * creates the git repo with a baseline commit on `main` (first run) or switches back to it
    and deletes old fix/* branches
  * gives the repo a remote called `origin` so "commit and push" really pushes:
      - default: a local "company server" repo in .demo-remote/ess-demo.git (no internet needed)
      - your own GitHub repo: python reset_demo.py --remote https://github.com/<you>/<repo>.git

Standard library only. Python 3.10+ and git.
"""
import argparse
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
LOCAL_REMOTE = ROOT / ".demo-remote" / "ess-demo.git"


def git(*args, check=True, cwd=ROOT):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and p.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {p.stderr.strip() or p.stdout.strip()}")
    return p


def rmtree(path):
    """shutil.rmtree that also removes git's read-only files on Windows."""
    def on_error(func, p, _exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)
    if path.exists():
        if sys.version_info >= (3, 12):
            shutil.rmtree(path, onexc=on_error)
        else:
            shutil.rmtree(path, onerror=on_error)


ap = argparse.ArgumentParser(description="Reset the ESS Claude Code demo")
ap.add_argument("--remote", help="use this URL as origin instead of the local demo remote (e.g. your GitHub repo)")
args = ap.parse_args()

if shutil.which("git") is None:
    sys.exit("git is not installed / not on PATH. Install Git for Windows from https://git-scm.com and retry.")

# 1) git: make sure we are on a clean `main`
if not (ROOT / ".git").exists():
    if git("init", "-b", "main", check=False).returncode != 0:  # older git
        git("init")
        git("checkout", "-b", "main")
    print("✔ created git repository")
else:
    # Discard uncommitted changes ONLY in app/ and tests/ - edits you made elsewhere are kept.
    git("checkout", "HEAD", "--", "app", "tests", check=False)
    if git("checkout", "main", check=False).returncode != 0:
        sys.exit("Could not switch to main. Commit or stash your changes, then run this again.")
    branches = [b.strip(" *") for b in git("branch", "--list", "fix/*", "feat/*", check=False).stdout.splitlines()]
    for b in filter(None, branches):
        git("branch", "-D", b, check=False)
    print("✔ switched back to main and removed old fix/* branches")

# 2) files: buggy app + no regression tests + empty guardrail log
(ROOT / "app" / "user_service.py").write_text(
    (ROOT / "demo_assets" / "user_service_buggy.py").read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
for f in (ROOT / "tests").glob("test_ess_*.py"):
    f.unlink()
log = ROOT / ".ess-ai" / "reports" / "guardrail-log.md"
if log.exists():
    log.unlink()
print("✔ restored the buggy app/user_service.py and removed old regression tests")

# 3) data + tickets: back to seed
shutil.copyfile(ROOT / "data" / "seed_users.json", ROOT / "data" / "users.json")
shutil.copyfile(ROOT / "jira_lite" / "seed_tickets.json", ROOT / "jira_lite" / "tickets.json")
print("✔ reset users (EMP1, EMP2, EMP3, EMP10, EMP11) and tickets (ESS-201, 202, 203 are in 'To Do')")

# 4) baseline commit
if not git("config", "user.name", check=False).stdout.strip():
    git("config", "user.name", "ESS Developer")
    print("  (git user.name was empty - set to 'ESS Developer' for this repo; change it with git config user.name)")
if not git("config", "user.email", check=False).stdout.strip():
    git("config", "user.email", "ess-developer@example.com")
git("add", "-A")
if git("diff", "--cached", "--quiet", check=False).returncode != 0:
    git("commit", "-m", "Baseline: ESS demo user management app with the ESS starter kit")
    print("✔ baseline commit created on main")

# 5) the remote that "commit and push" pushes to
current = git("remote", "get-url", "origin", check=False)
current_url = current.stdout.strip() if current.returncode == 0 else ""
if args.remote:
    if current_url:
        git("remote", "set-url", "origin", args.remote)
    else:
        git("remote", "add", "origin", args.remote)
    p = git("push", "-u", "origin", "main", check=False)
    print(f"✔ origin -> {args.remote}" + ("" if p.returncode == 0 else f"\n  ! push of main failed: {p.stderr.strip()}"))
elif current_url and Path(current_url).resolve() != LOCAL_REMOTE.resolve():
    print(f"✔ origin is your own remote ({current_url}); old fix/* branches there are not deleted."
          "\n  If a push is rejected because the branch already exists, delete it on the server first.")
else:
    rmtree(LOCAL_REMOTE)  # a fresh "company server" for every demo run
    git("init", "--bare", "-q", str(LOCAL_REMOTE), cwd=ROOT)
    if current_url:
        git("remote", "set-url", "origin", str(LOCAL_REMOTE))
    else:
        git("remote", "add", "origin", str(LOCAL_REMOTE))
    git("push", "-q", "-u", "origin", "main")
    git("fetch", "-q", "--prune", "origin", check=False)
    print("✔ origin -> .demo-remote/ess-demo.git (a local stand-in for the company git server; main pushed)")

print("\nReady. Next (each in its own VS Code terminal, with the .venv active):"
      "\n  python jira_lite/server.py   -> http://127.0.0.1:5055  (ticket board)"
      "\n  python app/server.py         -> http://127.0.0.1:5070  (the app with the bugs)"
      "\n  claude                       (Claude Code, in this folder)")
