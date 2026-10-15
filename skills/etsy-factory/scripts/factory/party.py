"""Party-game products: bingo, question cards (would you rather), multiple-choice trivia."""

import random

from .common import closing_page, cut_lines


def how_to_page(doc, title, steps, extra_title=None, extra=None):
    t, w, m = doc.t, doc.w, doc.m
    doc.new_page()
    y = doc.header(title, size=34)
    for i, step in enumerate(steps, 1):
        doc.circle(m + 34, y - 4, 14, fill=t["primary"])
        doc.text(m + 34, y - 9, str(i), "WorkSans-Bold", 13, "#FFFFFF", "center")
        y = doc.para(m + 62, y, step, "WorkSans-Regular", 17, w - 2 * m - 90, 24, t["ink"]) - 20
    if extra:
        y -= 10
        need = 70 + sum(len(doc.lines(e, "WorkSans-Regular", 15, w - 2 * m - 100)) * 21 + 10 for e in extra)
        doc.rect(m + 16, y - need, w - 2 * m - 32, need, fill=t["tint"], radius=14)
        yy = y - 34
        doc.text(w / 2, yy, extra_title, "Display", 22, t["primary"], "center")
        yy -= 30
        for e in extra:
            doc.ornament(m + 46, yy + 5, 5, t["secondary"])
            yy = doc.para(m + 62, yy, e, "WorkSans-Regular", 15, w - 2 * m - 100, 21, t["ink"]) - 10


# ---------------------------------------------------------------- bingo
def render_bingo(doc, spec, _built=None):
    t, w, h, m = doc.t, doc.w, doc.h, doc.m
    c = spec["content"]
    pool, n_cards = c["pool"], c.get("cards", 30)
    if len(pool) < 24 or len(set(pool)) != len(pool):
        raise SystemExit("bingo pool needs at least 24 unique entries")
    rng = random.Random(spec.get("seed", 7))
    cards, seen = [], set()
    while len(cards) < n_cards:
        pick = tuple(rng.sample(pool, 24))
        key = frozenset(pick)
        if key not in seen:
            seen.add(key)
            cards.append(pick)

    doc.cover(spec["cover_lines"], spec["subtitle"], spec["badges"])
    how_to_page(doc, "How to Play", [
        f"Print the {n_cards} bingo cards (one per player) and the calling cards. Cut the calling cards apart and put them in a bowl.",
        "Give each player a card and a few markers: candy, buttons, coins or a crayon all work.",
        "The caller draws one calling card at a time, reads it aloud, and ticks it on the caller's checklist.",
        "Players cover the matching square. The center square is free.",
        "The first player to complete a row, column or diagonal shouts BINGO! Check their card against the checklist.",
    ], "Ways to Play", c.get("variations", [
        "Four corners: cover all four corner squares.",
        "Picture frame: cover every square around the edge.",
        "Blackout: cover the whole card for a longer game.",
    ]))

    # caller checklist
    doc.new_page()
    y = doc.header("Caller's Checklist", size=30)
    cols = 2
    rows = -(-len(pool) // cols)
    row_h = min(30, (y - m - 20) / rows)
    col_w = (w - 2 * m - 40) / cols
    for i, word in enumerate(sorted(pool)):
        col, row = divmod(i, rows)
        x = m + 30 + col * col_w
        yy = y - row * row_h
        doc.checkbox(x, yy - 2, 13, t["primary"])
        doc.text(x + 22, yy, word, "WorkSans-Regular", 14, t["ink"], max_w=col_w - 30)

    # cards
    letters = c.get("header_letters", "BINGO")
    colors = [t["primary"], t["secondary"], t["accent"], t["primary"], t["secondary"]]
    grid_w = min(w - 2 * m - 20, h - 2 * m - 190)
    cell = grid_w / 5
    for k, card in enumerate(cards, 1):
        doc.new_page()
        top = h - m
        doc.text(w / 2, top - 44, c["card_title"], "Display", 40, t["primary"], "center", max_w=w - 2 * m)
        tw = doc.c.stringWidth(c["card_title"], "Display", 40) / 2 + 26
        doc.ornament(w / 2 - tw, top - 30, 10, t["accent"])
        doc.ornament(w / 2 + tw, top - 30, 10, t["accent"])
        x0 = (w - grid_w) / 2
        hy = top - 106
        for i, L in enumerate(letters):
            cx = x0 + cell * (i + 0.5)
            doc.circle(cx, hy, cell * 0.33, fill=colors[i])
            doc.text(cx, hy - 11, L, "Head", 30, "#FFFFFF", "center")
        gy = hy - cell * 0.45
        doc.rect(x0 - 6, gy - 5 * cell - 6, grid_w + 12, 5 * cell + 12, stroke=t["primary"], width=2.2, radius=10)
        words = list(card)
        words.insert(12, None)
        for i, word in enumerate(words):
            r, col = divmod(i, 5)
            x, ytop = x0 + col * cell, gy - r * cell
            doc.rect(x, ytop - cell, cell, cell, stroke=t["primary"], width=0.9)
            if word is None:
                doc.rect(x + 3, ytop - cell + 3, cell - 6, cell - 6, fill=t["tint"])
                doc.ornament(x + cell / 2, ytop - cell * 0.42, cell * 0.2, t["secondary"])
                doc.text(x + cell / 2, ytop - cell * 0.82, c.get("free_label", "FREE"), "WorkSans-Bold", 12, t["primary"], "center")
            else:
                doc.para_fit(x + 7, ytop - 7, word, "WorkSans-Bold", 17, cell - 14, cell - 14, t["ink"])
        doc.text(w / 2, gy - 5 * cell - 34, f"Card {k}", "WorkSans-Regular", 11, t["muted"], "center")

    # calling cards to cut out
    per_cols, per_rows = 4, 5
    per = per_cols * per_rows
    for start in range(0, len(pool), per):
        doc.new_page()
        top = doc.header("Calling Cards", "Cut along the dashed lines", size=26)
        bottom = m + 12
        cut_lines(doc, per_cols, per_rows, top, bottom)
        cw, ch = (w - 2 * m) / per_cols, (top - bottom) / per_rows
        for k, word in enumerate(pool[start:start + per]):
            r, col = divmod(k, per_cols)
            x, ytop = m + col * cw, top - r * ch
            doc.ornament(x + cw / 2, ytop - 18, 6, t["accent"])
            doc.para_fit(x + 10, ytop - 26, word, "WorkSans-Bold", 18, cw - 20, ch - 36, t["primary"])
    closing_page(doc, spec)


# ---------------------------------------------------------------- question cards
def cap(s):
    return s[:1].upper() + s[1:]


def render_cards(doc, spec, _built=None):
    t, w, h, m = doc.t, doc.w, doc.h, doc.m
    c = spec["content"]
    qs = c["questions"]
    doc.cover(spec["cover_lines"], spec["subtitle"], spec["badges"])
    how_to_page(doc, "How to Play", c["rules"], "Play It Your Way", c.get("variations"))

    # question list sheets
    per = 15
    for start in range(0, len(qs), per):
        doc.new_page()
        y = doc.header(c["card_title"], c.get("list_subtitle"), size=30) - 12
        row_h = (y - m - 10) / per
        for i, (a, b) in enumerate(qs[start:start + per], start + 1):
            yy = y - (i - start - 1) * row_h
            doc.circle(m + 20, yy - 4, 12, fill=t["primary"] if i % 2 else t["secondary"])
            doc.text(m + 20, yy - 8.5, str(i), "WorkSans-Bold", 10.5, "#FFFFFF", "center")
            doc.para(m + 42, yy - 0, f"{cap(a)} or {b}?", "WorkSans-Regular", 13.5, w - 2 * m - 50, 16.5, t["ink"])

    # cut-out cards, 2 x 4 per page
    cols, rows = 2, 4
    for start in range(0, len(qs), cols * rows):
        doc.new_page()
        top, bottom = h - m, m + 8
        cut_lines(doc, cols, rows, top, bottom)
        cw, ch = (w - 2 * m) / cols, (top - bottom) / rows
        for k, (a, b) in enumerate(qs[start:start + cols * rows]):
            r, col = divmod(k, cols)
            x, ytop = m + col * cw, top - r * ch
            doc.rect(x + 8, ytop - ch + 8, cw - 16, ch - 16, stroke=t["accent"], width=1.2, radius=10)
            doc.text(x + cw / 2, ytop - 32, c["card_title"] + "...", "Display", 16, t["primary"], "center", max_w=cw - 40)
            box_h = (ch - 70) / 2 - 10
            doc.para_fit(x + 22, ytop - 44, cap(a), "WorkSans-Bold", 16, cw - 44, box_h, t["ink"])
            mid = ytop - 44 - box_h - 10
            doc.line(x + 40, mid, x + cw / 2 - 18, mid, t["accent"], 0.8)
            doc.line(x + cw / 2 + 18, mid, x + cw - 40, mid, t["accent"], 0.8)
            doc.text(x + cw / 2, mid - 4, "or", "Lora-Italic", 13, t["secondary"], "center")
            doc.para_fit(x + 22, mid - 10, cap(b), "WorkSans-Bold", 16, cw - 44, box_h, t["ink"])
            doc.text(x + cw - 22, ytop - ch + 18, str(start + k + 1), "WorkSans-Regular", 8, t["muted"], "right")
    closing_page(doc, spec)


# ---------------------------------------------------------------- trivia
def render_trivia(doc, spec, _built=None):
    t, w, h, m = doc.t, doc.w, doc.h, doc.m
    c = spec["content"]
    rounds = c["rounds"]
    for rd in rounds:
        for q in rd["questions"]:
            if len(q["options"]) != 4 or q["answer"] not in "ABCD":
                raise SystemExit(f"Trivia question needs 4 options and an answer A-D: {q['q']}")
    doc.cover(spec["cover_lines"], spec["subtitle"], spec["badges"])
    total = sum(len(r["questions"]) for r in rounds)
    how_to_page(doc, "How to Play", [
        "Split into teams of two to six players, or play as individuals. Give each team an answer sheet and a pen.",
        f"The host reads each question and its four choices aloud. There are {len(rounds)} rounds and {total} questions.",
        "Teams quietly write the letter of their answer. No phones!",
        "After each round, the host reads the answers from the answer key and teams swap sheets to mark them.",
        "Score one point per correct answer. Record totals on the scoreboard. Most points wins.",
    ], "Host Tips", [
        "Let the youngest player read a question each round.",
        "Tie? Ask everyone to guess how many lights are on the biggest tree in the room. Closest wins." if spec["theme"] == "christmas"
        else "Tie? Each team guesses a number the host picks between 1 and 100. Closest wins.",
        "Print the question pages for the host, and one answer sheet per team.",
    ])
    letters = "ABCD"
    for ri, rd in enumerate(rounds, 1):
        doc.new_page()
        y = doc.header(f"Round {ri}: {rd['title']}", size=26)
        qn = len(rd["questions"])
        row_h = (y - m - 6) / qn
        for qi, q in enumerate(rd["questions"], 1):
            yy = y - (qi - 1) * row_h
            doc.text(m + 6, yy, f"{qi}.", "WorkSans-Bold", 13, t["secondary"])
            y2 = doc.para(m + 30, yy, q["q"], "WorkSans-Bold", 12.5, w - 2 * m - 36, 15.5, t["ink"]) - 3
            opt_w = (w - 2 * m - 36) / 2
            for oi, opt in enumerate(q["options"]):
                col, row = oi % 2, oi // 2
                doc.text(m + 30 + col * opt_w, y2 - row * 15, f"{letters[oi]})  {opt}", "WorkSans-Regular", 11.5,
                         t["ink"], max_w=opt_w - 10)

    # answer sheet for teams
    doc.new_page()
    y = doc.header("Team Answer Sheet", size=28)
    doc.text(m + 10, y - 8, "Team name:", "WorkSans-Bold", 13, t["primary"])
    doc.line(m + 95, y - 10, w - m - 10, y - 10, t["muted"], 0.8)
    y -= 40
    cols = len(rounds)
    col_w = (w - 2 * m) / cols
    maxq = max(len(r["questions"]) for r in rounds)
    row_h = min(44, (y - m - 70) / (maxq + 1))
    for ri, rd in enumerate(rounds):
        x = m + ri * col_w
        doc.rect(x + 4, y - 26, col_w - 8, 26, fill=t["primary"] if ri % 2 == 0 else t["secondary"], radius=6)
        doc.text(x + col_w / 2, y - 18, f"Round {ri + 1}", "WorkSans-Bold", 12, "#FFFFFF", "center")
        for qi in range(len(rd["questions"])):
            yy = y - 26 - (qi + 1) * row_h
            doc.text(x + 14, yy + 6, f"{qi + 1}.", "WorkSans-Regular", 11, t["muted"])
            doc.line(x + 34, yy + 4, x + col_w - 14, yy + 4, t["muted"], 0.6)
        yy = y - 26 - (maxq + 1) * row_h - 4
        doc.text(x + 14, yy + 6, "Score:", "WorkSans-Bold", 10, t["primary"])
        doc.rect(x + 54, yy, col_w - 68, 22, stroke=t["primary"], width=0.9, radius=4)

    # answer key
    doc.new_page()
    y = doc.header("Answer Key", "For the host only. No peeking!", size=28)
    half = (w - 2 * m) / 2
    per_col = -(-len(rounds) // 2)
    block_h = (y - m) / per_col
    for ri, rd in enumerate(rounds):
        col, row = divmod(ri, per_col)
        x, yy = m + col * half + 8, y - row * block_h
        doc.text(x, yy - 4, f"Round {ri + 1}: {rd['title']}", "WorkSans-Bold", 12.5, t["primary"], max_w=half - 20)
        line_h = min(17, (block_h - 30) / len(rd["questions"]))
        for qi, q in enumerate(rd["questions"]):
            ai = letters.index(q["answer"])
            doc.text(x + 4, yy - 24 - qi * line_h, f"{qi + 1}.  {q['answer']}  {q['options'][ai]}", "WorkSans-Regular", 10.5,
                     t["ink"], max_w=half - 30)

    # scoreboard
    doc.new_page()
    y = doc.header("Scoreboard", size=32)
    teams = 8
    cols = len(rounds) + 2
    first = (w - 2 * m) * 0.3
    cw = (w - 2 * m - first) / (cols - 1)
    row_h = min(48, (y - m - 20) / (teams + 1))
    heads = ["Team"] + [f"R{i + 1}" for i in range(len(rounds))] + ["Total"]
    for i, hd in enumerate(heads):
        x = m if i == 0 else m + first + (i - 1) * cw
        wd = first if i == 0 else cw
        doc.rect(x, y - row_h, wd, row_h, fill=t["primary"], stroke="#FFFFFF", width=1)
        doc.text(x + wd / 2, y - row_h / 2 - 5, hd, "WorkSans-Bold", 13, "#FFFFFF", "center")
    for r in range(teams):
        yy = y - (r + 2) * row_h
        for i in range(cols):
            x = m if i == 0 else m + first + (i - 1) * cw
            wd = first if i == 0 else cw
            doc.rect(x, yy, wd, row_h, fill=t["tint"] if r % 2 == 0 else None, stroke=t["muted"], width=0.6)
    closing_page(doc, spec)
