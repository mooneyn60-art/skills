<!-- Routine: TARS weekly desk reset | schedule: 0 13 * * 6 (UTC) = Sat 9am ET | runs in: main session -->

# Weekly desk reset

Why: every hourly check adds to the trading desk's context. After one day it
was ~260k tokens and had cost ~$34, because every check re-reads everything
said before. A fresh desk starts at ~80k. Everything the desk needs lives in
the repo and the broker, not its memory, so nothing is lost.

Runs Saturday morning: market closed, no hourly checks firing.
Needs the Claude_Code_Remote tools (create_session, create_trigger,
delete_trigger, list_triggers, get_session, archive_session).

## Steps, in order. Stop and tell Nolan if any step fails.

1. list_triggers. Find the OLD desk id: the persistent_session_id on
   "TARS — hourly trading check (desk)". Collect EVERY enabled trigger with
   that persistent_session_id (hourly, Friday refresh, and any one-shots
   such as the SOFI brief or gut-call scoring). Save name, cron or
   run_once_at, and prompt for each (get_trigger shows the prompt).
   Skip one-shots whose time has already passed.
2. get_session on the old desk. If it's mid-turn (status running), wait and
   retry. Never swap during a live check.
3. create_session:
     title "TARS trading desk (week of YYYY-MM-DD)"
     source_url https://github.com/mooneyn60-art/skills
     source_revision and outcome_branch claude/package-installation-setup-yv4j79
     permission_mode auto
     prompt: "You are the TARS trading desk. Scheduled routines will fire
     into this session. Run git pull, read
     skills/robinhood-autotrader/routines/HOURLY_TRADING_CHECK.md, then do a
     READ-ONLY verification: list positions and open orders on #731951265 and
     confirm every position has its stop. NO ORDERS this turn. Reply in 3
     lines or fewer."
4. Wait for it to go idle, then get_session. Its post_turn_summary must
   show it read the account (positions/stops). If it has no broker tools
   or no repo, STOP: leave the old triggers alone and tell Nolan.
5. For each trigger from step 1: create_trigger with the SAME name, schedule
   and prompt, persistent_session_id = the new desk, initiation
   human_schedule. Confirm each returns an id.
6. Only after ALL new triggers exist: delete_trigger each old one.
7. archive_session the old desk.
8. Tell Nolan in 2 lines: new desk id, triggers moved, old desk archived.
   Update the session ids in routines/README.md if they are listed, then commit.

R13 applies to the commit message.
