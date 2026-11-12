#!/usr/bin/env python3
"""PreToolUse hook for Bash: stop git commands that wipe or sweep up uncommitted work.

Why it exists: on 2026-11-12 a review agent's failed `cd` ran a commit and `git checkout -- .` inside the
real repo and four uncommitted files were lost (MASTER_ORDERS, "Agent routing"; research 94, section 6).

Rules for everyone:
  - no whole-tree checkout or restore (`git checkout -- .`, `git checkout -f`, `git restore .`)
  - no `git reset --hard`, `git clean`, `git stash` (list and show are fine)
  - no `git sparse-checkout reapply|set|disable|init` (they delete files outside the patterns; `add` is fine)
  - no `git add -A`, `git add --all`, `git add .`, `git commit -a` (CLAUDE.md: add paths with `git add --sparse`)
Extra rule for subagents (the hook input carries an agent id): no git command that changes the repo at all.
The main session commits.

Text inside quotes and heredocs is ignored, so a commit message or a note may mention these commands.
Test: echo '{"tool_name":"Bash","tool_input":{"command":"git checkout -- ."}}' | python3 .claude/hooks/git-guard.py
"""
import json
import re
import sys

WRITE_SUBCOMMANDS = {"add", "commit", "push", "checkout", "switch", "restore", "reset", "rm", "mv", "apply", "am",
                     "merge", "rebase", "cherry-pick", "revert", "stash", "clean", "worktree", "tag", "pull",
                     "update-index", "update-ref", "gc", "prune", "filter-branch", "replace"}


def strip_quoted(cmd):
    """Drop heredoc bodies and quoted strings, so only the commands themselves are judged."""
    out, lines, i = [], cmd.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        m = re.search(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1", line)
        if m:
            end = m.group(2)
            i += 1
            while i < len(lines) and lines[i].strip() != end:
                i += 1
        i += 1
    text = "\n".join(out)
    text = re.sub(r"'[^']*'", "''", text)
    text = re.sub(r'"(?:\\.|[^"\\])*"', '""', text)
    return text


def git_calls(cmd):
    """Yield (subcommand, rest) for each git call in a compound command."""
    for seg in re.split(r"&&|\|\||;|\||\n|\$\(|`|\(|\)", strip_quoted(cmd)):
        m = re.search(r"(?:^|\s)git((?:\s+(?:-[cC]\s+\S+|--git-dir(?:=|\s+)\S+|--work-tree(?:=|\s+)\S+|--no-pager|-P))*)\s+([a-z][a-z-]*)(.*)$",
                      seg.strip(), re.S)
        if m:
            yield m.group(2), " " + m.group(3).strip() + " "


def danger(sub, rest):
    has = lambda pat: re.search(pat, rest) is not None
    if sub == "checkout" and (has(r"\s(-f|--force)\s") or has(r"\s--\s+(\.|:/|\*)\s") or has(r"^\s+(\.|:/)\s")
                              or has(r"^\s+\S+\s+(\.|:/)\s")):
        return "a whole-tree `git checkout` throws away every uncommitted change"
    if sub == "restore" and has(r"\s(\.|:/|\*)\s"):
        return "a whole-tree `git restore` throws away every uncommitted change"
    if sub == "reset" and has(r"\s--hard\s"):
        return "`git reset --hard` throws away every uncommitted change (use --soft or --mixed)"
    if sub == "clean" and not has(r"\s(-n|--dry-run)\s") and not has(r"\s-[a-zA-Z]*n[a-zA-Z]*\s"):
        return "`git clean` deletes untracked files (new research and renders are untracked until committed)"
    if sub == "stash" and not has(r"^\s+(list|show)\s"):
        return "`git stash` hides uncommitted work where the next session will not find it"
    if sub == "sparse-checkout" and has(r"^\s+(reapply|set|disable|init)\s"):
        return "this sparse-checkout command deletes files outside the patterns (use `git sparse-checkout add <path>`)"
    if sub == "add" and (has(r"\s(-A|--all)\s") or has(r"\s\.\s") or has(r"\s-[a-zA-Z]*A[a-zA-Z]*\s")):
        return "never `git add -A` or `git add .` here: add paths with `git add --sparse <paths>` (CLAUDE.md)"
    if sub == "commit" and (has(r"\s(-a|--all)\s") or has(r"\s-[b-zB-Z]*a[a-zA-Z]*\s")):
        return "never `git commit -a` here: add paths with `git add --sparse <paths>`, then commit (CLAUDE.md)"
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if data.get("tool_name") != "Bash":
        return
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if "git" not in cmd:
        return
    in_subagent = bool(data.get("agent_id"))
    for sub, rest in git_calls(cmd):
        why = danger(sub, rest)
        if not why and in_subagent:
            if sub in WRITE_SUBCOMMANDS or (sub == "sparse-checkout" and not re.search(r"^\s+list\s", rest)) \
                    or (sub == "branch" and re.search(r"\s-[dDmMcC]\s", rest)):
                why = "agents never change the repo with git; the main session commits (MASTER_ORDERS, Agent routing)"
        if why:
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse", "permissionDecision": "deny",
                "permissionDecisionReason": "Blocked by .claude/hooks/git-guard.py: git %s: %s." % (sub, why)}}))
            return


if __name__ == "__main__":
    main()
