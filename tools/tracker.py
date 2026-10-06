#!/usr/bin/env python3
"""ESS Tracker CLI: how Claude Code (and you) talk to the ticket board at http://127.0.0.1:5055.

  python tools/tracker.py list                       open tickets, highest priority first
  python tools/tracker.py show ESS-201               the full ticket
  python tools/tracker.py start ESS-201              card -> In Progress, assigned to Claude Code,
                                                     and the repo back on a clean main branch
  python tools/tracker.py comment ESS-201 "text"     add a comment to the card
  python tools/tracker.py move ESS-201 "To Do"       move the card (To Do / In Progress / In Review / Done)
  python tools/tracker.py shipped ESS-201 --evidence file.json
                                                     called by tools/ess_ship.py after the push:
                                                     card -> In Review with branch, commit, tests and diff

In a real project this is your Jira / Azure DevOps API or MCP connector; the workflow stays the same.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOARD = os.environ.get("JIRA_LITE_URL", "http://127.0.0.1:5055")
AUTHOR = "Claude Code"
ORDER = {"Highest": 0, "High": 1, "Medium": 2, "Low": 3}


def api(method: str, path: str, body: dict | None = None) -> dict | list:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        BOARD + path, data=data, method=method, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:  # noqa: S310 - local demo board
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        sys.exit(f"Tracker said {exc.code}: {exc.read().decode('utf-8', 'replace')}")
    except (urllib.error.URLError, OSError):
        sys.exit(f"Cannot reach the ticket board at {BOARD}. Start it: python jira_lite/server.py")


def git(*args: str) -> tuple[int, str]:
    p = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return p.returncode, (p.stdout + p.stderr).strip()


def cmd_list(_: argparse.Namespace) -> None:
    tickets = sorted(api("GET", "/api/tickets"), key=lambda t: (t["status"] == "Done", ORDER.get(t["priority"], 9)))
    for t in tickets:
        print(f"{t['id']:<9} {t['status']:<12} {t['priority']:<8} {t['type']:<6} {t['title']}")


def cmd_show(a: argparse.Namespace) -> None:
    t = api("GET", f"/api/tickets/{a.ticket}")
    print(f"{t['id']}  [{t['type']} | {t['priority']} | {t['status']}]  {t['title']}")
    print(f"Reporter: {t.get('reporter', '-')}   Component: {t.get('component', '-')}\n")
    print(f"Description:\n  {t.get('description', '')}\n")
    if t.get("steps"):
        print("Steps to reproduce:")
        for i, s in enumerate(t["steps"], 1):
            print(f"  {i}. {s}")
        print()
    print(f"Expected: {t.get('expected', '')}")
    print(f"Actual:   {t.get('actual', '')}\n")
    print("Acceptance criteria:")
    for c in t.get("acceptance_criteria", []):
        print(f"  - {c}")
    if t.get("comments"):
        print("\nComments:")
        for c in t["comments"]:
            print(f"  [{c['time']}] {c['author']}: {c['body']}")


def cmd_start(a: argparse.Namespace) -> None:
    t = api("GET", f"/api/tickets/{a.ticket}")
    code, branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if code == 0 and branch != "main":
        _, dirty = git("status", "--porcelain", "--untracked-files=no")
        if dirty:
            print(f"Note: you are on {branch} with uncommitted changes, so the branch was not switched.")
        else:
            git("checkout", "-q", "main")
            print(f"Switched from {branch} back to main (each ticket gets its own branch from main).")
    api("PATCH", f"/api/tickets/{t['id']}", {"status": "In Progress", "assignee": AUTHOR})
    api(
        "POST",
        f"/api/tickets/{t['id']}/comments",
        {"author": AUTHOR, "body": "Picked up in Claude Code (VS Code). Analysing the code before any change."},
    )
    print(f"{t['id']} is now In Progress, assigned to {AUTHOR}.")


def cmd_comment(a: argparse.Namespace) -> None:
    api("POST", f"/api/tickets/{a.ticket}/comments", {"author": AUTHOR, "body": a.text})
    print(f"Comment added to {a.ticket.upper()}.")


def cmd_move(a: argparse.Namespace) -> None:
    api("PATCH", f"/api/tickets/{a.ticket}", {"status": a.status})
    print(f"{a.ticket.upper()} moved to {a.status}.")


def cmd_shipped(a: argparse.Namespace) -> None:
    ev = json.loads(Path(a.evidence).read_text(encoding="utf-8"))
    tid = ev["ticket"]
    changes = {
        "branch": ev["branch"],
        "commit": ev["commit"],
        "tests": ev["tests"],
        "files": ev["files"],
        "diff": ev["diff"],
        "pushed": ev["pushed"],
        "remote": ev.get("remote", ""),
        "pr": ev.get("pr", ""),
        "approved_by": ev.get("approved_by", ""),
    }
    api("PATCH", f"/api/tickets/{tid}", {"status": "In Review", "changes": changes})
    where = f"pushed to origin/{ev['branch']}" if ev["pushed"] else f"committed on {ev['branch']} (not pushed)"
    body = (
        f"Fix {where}.\nCommit {ev['commit']}: {ev['title']}\nTests: {ev['tests']}\n"
        f"Files: {', '.join(ev['files'])}\nApproved in Claude Code by {ev.get('approved_by', 'the developer')}."
        + (f"\nPR: {ev['pr']}" if ev.get("pr") else "")
        + "\nPlease review the diff and approve."
    )
    api("POST", f"/api/tickets/{tid}/comments", {"author": AUTHOR, "body": body})
    print(f"{tid} moved to In Review on the board with the diff.")


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(prog="tracker.py", description="ESS Tracker CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    for name, fn in (("show", cmd_show), ("start", cmd_start)):
        p = sub.add_parser(name)
        p.add_argument("ticket")
        p.set_defaults(fn=fn)
    p = sub.add_parser("comment")
    p.add_argument("ticket")
    p.add_argument("text")
    p.set_defaults(fn=cmd_comment)
    p = sub.add_parser("move")
    p.add_argument("ticket")
    p.add_argument("status", choices=["To Do", "In Progress", "In Review", "Done"])
    p.set_defaults(fn=cmd_move)
    p = sub.add_parser("shipped")
    p.add_argument("ticket")
    p.add_argument("--evidence", required=True)
    p.set_defaults(fn=cmd_shipped)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
