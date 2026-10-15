"""Planner and classroom products: job charts, budget pages and meal-planning pages."""

from .common import closing_page
from .kit import hexc

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def table(doc, x, y_top, widths, row_h, headers, n_rows, first_col=None, check_col=None, fill=None, size=10.5):
    """Header row plus n_rows blank rows; returns the y of the table bottom."""
    t = doc.t
    fill = fill or t["primary"]
    total = sum(widths)
    doc.rect(x, y_top - row_h, total, row_h, fill=fill, radius=0)
    cx = x
    for wd, hd in zip(widths, headers):
        doc.text(cx + wd / 2, y_top - row_h / 2 - size * 0.35, hd, "WorkSans-Bold", size, "#FFFFFF", "center", max_w=wd - 6)
        cx += wd
    for r in range(n_rows):
        yy = y_top - (r + 2) * row_h
        if r % 2 == 0:
            doc.rect(x, yy, total, row_h, fill=t["tint"])
        if first_col:
            label = first_col[r] if r < len(first_col) else ""
            doc.text(x + 6, yy + row_h / 2 - 4, label, "WorkSans-Bold", size, t["ink"], max_w=widths[0] - 10)
        if check_col is not None:
            ccx = x + sum(widths[:check_col]) + widths[check_col] / 2
            s = min(11, row_h * 0.55)
            doc.checkbox(ccx - s / 2, yy + (row_h - s) / 2, s, t["primary"])
    bottom = y_top - (n_rows + 1) * row_h
    cx = x
    for wd in widths[:-1]:
        cx += wd
        doc.line(cx, y_top - row_h, cx, bottom, t["muted"], 0.4)
    doc.rect(x, bottom, total, (n_rows + 1) * row_h, stroke=fill, width=1)
    return bottom


def section_title(doc, x, y, label, color=None):
    doc.text(x, y, label.upper(), "WorkSans-Bold", 11.5, color or doc.t["secondary"])
    return y - 8


def write_line(doc, x, y, label, width):
    doc.text(x, y, label, "WorkSans-Bold", 11, doc.t["primary"])
    lw = doc.c.stringWidth(label, "WorkSans-Bold", 11) + 6
    doc.line(x + lw, y - 2, x + width, y - 2, doc.t["muted"], 0.7)


# ------------------------------------------------------------- classroom jobs
def render_jobs(doc, spec, _built=None):
    t, w, h, m = doc.t, doc.w, doc.h, doc.m
    c = spec["content"]
    jobs = c["jobs"] + [{"name": "", "duty": ""}] * c.get("blank_cards", 6)
    cyc = t["cycle"]
    doc.cover(spec["cover_lines"], spec["subtitle"], spec["badges"])

    # how to use
    doc.new_page()
    y = doc.header("How to Use", size=34)
    for p in c["how_to"]:
        doc.ornament(m + 22, y - 5, 7, t["accent"], "star")
        y = doc.para(m + 40, y, p, "WorkSans-Regular", 14.5, w - 2 * m - 60, 20, t["ink"]) - 12

    # bunting letters, 2 pennants per page
    word = [ch for ch in c.get("banner", "CLASSROOM JOBS") if ch != " "]
    for start in range(0, len(word), 2):
        doc.new_page(footer=False)
        pw = (w - 2 * m - 20) / 2
        for k, ch in enumerate(word[start:start + 2]):
            x0 = m + k * (pw + 20)
            top = h - m - 30
            color = cyc[(start + k) % len(cyc)]
            p = doc.c.beginPath()
            p.moveTo(x0, top)
            p.lineTo(x0 + pw, top)
            p.lineTo(x0 + pw / 2, top - pw * 1.45)
            p.close()
            doc.c.setFillColor(hexc(color))
            doc.c.drawPath(p, stroke=0, fill=1)
            doc.circle(x0 + pw / 2, top - pw * 0.48, pw * 0.3, fill="#FFFFFF")
            doc.text(x0 + pw / 2, top - pw * 0.48 - 40, ch, "Head", 115, color, "center")
            doc.circle(x0 + 18, top - 14, 4, fill="#FFFFFF")
            doc.circle(x0 + pw - 18, top - 14, 4, fill="#FFFFFF")
        doc.text(w / 2, m, "Cut out, punch the two holes and string together.", "WorkSans-Italic", 9, t["muted"], "center")

    # job cards, 2 x 3 per page
    cols, rows = 2, 3
    gap = 16
    cw = (w - 2 * m - gap) / cols
    ch = (h - 2 * m - 10 - gap * (rows - 1)) / rows
    for start in range(0, len(jobs), cols * rows):
        doc.new_page()
        for k, job in enumerate(jobs[start:start + cols * rows]):
            r, col = divmod(k, cols)
            x = m + col * (cw + gap)
            ytop = h - m - r * (ch + gap)
            color = cyc[(start + k) % len(cyc)]
            doc.rect(x, ytop - ch, cw, ch, fill="#FFFFFF", stroke=color, width=3, radius=14)
            doc.rect(x, ytop - 58, cw, 58, fill=color, radius=14)
            doc.rect(x, ytop - 58, cw, 20, fill=color)
            doc.ornament(x + 22, ytop - 29, 8, "#FFFFFF", "star")
            doc.ornament(x + cw - 22, ytop - 29, 8, "#FFFFFF", "star")
            if job["name"]:
                doc.text(x + cw / 2, ytop - 38, job["name"], "Head", 24, "#FFFFFF", "center", max_w=cw - 70)
                doc.para_fit(x + 18, ytop - 66, job["duty"], "WorkSans-Regular", 13, cw - 36, ch - 140, t["ink"])
            else:
                doc.line(x + 40, ytop - 40, x + cw - 40, ytop - 40, "#FFFFFF", 1.2, dash=(2, 3))
                for j in range(2):
                    doc.line(x + 20, ytop - 90 - j * 24, x + cw - 20, ytop - 90 - j * 24, t["muted"], 0.6, dash=(2, 3))
            doc.rect(x + 16, ytop - ch + 14, cw - 32, 46, fill=t["tint"], radius=10)
            doc.text(x + 28, ytop - ch + 44, "Name", "WorkSans-Bold", 9, color)
            doc.line(x + 28, ytop - ch + 26, x + cw - 28, ytop - ch + 26, t["muted"], 0.7, dash=(2, 3))

    # weekly rotation chart
    doc.new_page()
    y = doc.header("Job Rotation Chart", "Write a name in each week's column", size=28)
    names = [j["name"] for j in c["jobs"]][:24]
    first = (w - 2 * m) * 0.3
    rest = (w - 2 * m - first) / 4
    table(doc, m, y, [first] + [rest] * 4, min(24, (y - m - 10) / (len(names) + 1)),
          ["Job", "Week 1", "Week 2", "Week 3", "Week 4"], len(names), first_col=names)
    closing_page(doc, spec)


# ------------------------------------------------------------- planner pages
def p_monthly_budget(doc, page):
    t, w, m = doc.t, doc.w, doc.m
    y = doc.header(page.get("title", "Monthly Budget"), size=28)
    write_line(doc, m, y - 6, "Month:", (w - 2 * m) / 2 - 20)
    write_line(doc, w / 2 + 10, y - 6, "Year:", (w - 2 * m) / 2 - 10)
    y -= 30
    full = w - 2 * m
    y = section_title(doc, m, y, "Income")
    y = table(doc, m, y, [full * 0.5, full * 0.25, full * 0.25], 19, ["Source", "Expected", "Actual"], 4) - 18
    y = section_title(doc, m, y, "Bills and fixed expenses")
    y = table(doc, m, y, [full * 0.4, full * 0.14, full * 0.18, full * 0.18, full * 0.1], 19,
              ["Bill", "Due", "Budget", "Actual", "Paid"], 9, check_col=4) - 18
    y = section_title(doc, m, y, "Everyday spending")
    half = (full - 16) / 2
    y2 = table(doc, m, y, [half * 0.5, half * 0.25, half * 0.25], 19, ["Category", "Budget", "Actual"], 6,
               first_col=["Groceries", "Household", "Eating out", "Kids", "Personal care", "Fun money"])
    bx = m + half + 16
    doc.rect(bx, y2, half, y - y2, fill=t["tint"], radius=10)
    lines = ["Total income", "Total bills", "Total spending", "Savings", "Left over"]
    step = (y - y2 - 20) / len(lines)
    for i, lab in enumerate(lines):
        yy = y - 22 - i * step
        doc.text(bx + 14, yy, lab, "WorkSans-Bold", 11, t["primary"])
        doc.text(bx + half * 0.58, yy, "$", "WorkSans-Regular", 11, t["muted"])
        doc.line(bx + half * 0.58 + 10, yy - 2, bx + half - 14, yy - 2, t["muted"], 0.7)
    y = y2 - 16
    section_title(doc, m, y, "Notes")
    for i in range(int((y - m - 30) // 20)):
        doc.line(m, y - 26 - i * 20, w - m, y - 26 - i * 20, t["muted"], 0.5)


def p_bill_tracker(doc, page):
    w, m = doc.w, doc.m
    y = doc.header(page.get("title", "Bill Payment Tracker"), "Tick each bill as you pay it", size=28)
    full = w - 2 * m
    first, due = full * 0.22, full * 0.08
    mw = (full - first - due) / 12
    rows = int((y - m - 20) // 24) - 1
    bottom = table(doc, m, y, [first, due] + [mw] * 12, 24, ["Bill", "Due"] + MONTHS, rows, size=9.5)
    for r in range(rows):
        yy = y - (r + 2) * 24
        for k in range(12):
            cx = m + first + due + mw * (k + 0.5)
            doc.checkbox(cx - 5, yy + 7, 10, doc.t["primary"])
    return bottom


def p_sinking_funds(doc, page):
    t, w, h, m = doc.t, doc.w, doc.h, doc.m
    y = doc.header(page.get("title", "Sinking Funds"), "Color in one box for every 5% you save", size=28)
    cols, rows, gap = 2, 3, 14
    cw = (w - 2 * m - gap) / cols
    ch = (y - m - gap * (rows - 1)) / rows
    for k in range(cols * rows):
        r, col = divmod(k, cols)
        x, ytop = m + col * (cw + gap), y - r * (ch + gap)
        doc.rect(x, ytop - ch, cw, ch, stroke=t["accent"], width=1.3, radius=12, fill="#FFFFFF")
        write_line(doc, x + 12, ytop - 22, "Saving for:", cw - 24)
        write_line(doc, x + 12, ytop - 44, "Goal $", cw / 2 - 16)
        write_line(doc, x + cw / 2 + 4, ytop - 44, "By:", cw / 2 - 16)
        bs = (cw - 24 - 9 * 4) / 10
        for i in range(20):
            rr, cc = divmod(i, 10)
            bx = x + 12 + cc * (bs + 4)
            by = ytop - 64 - (rr + 1) * (bs + 4)
            doc.rect(bx, by, bs, bs, stroke=t["primary"], width=0.8, radius=3)
            doc.text(bx + bs / 2, by + bs / 2 - 3, f"{(i + 1) * 5}", "WorkSans-Regular", 6.5, t["muted"], "center")
        ly = ytop - 64 - 2 * (bs + 4) - 16
        cw3 = (cw - 24) / 3
        for j, hd in enumerate(["Date", "Added", "Balance"]):
            doc.text(x + 12 + cw3 * (j + 0.5), ly, hd, "WorkSans-Bold", 9, t["secondary"], "center")
        n = int((ly - (ytop - ch) - 12) // 17)
        for i in range(n):
            doc.line(x + 12, ly - 12 - i * 17, x + cw - 12, ly - 12 - i * 17, t["muted"], 0.5)


def p_savings_challenge(doc, page):
    t, w, m = doc.t, doc.w, doc.m
    y = doc.header(page.get("title", "$1,000 Savings Challenge"), "Color in a circle each time you save that amount", size=28)
    amounts = [10] * 20 + [25] * 20 + [30] * 10
    order = sorted(range(50), key=lambda i: (i * 37) % 50)
    amounts = [amounts[i] for i in order]
    cols, rows = 7, 8
    cw = (w - 2 * m) / cols
    rh = (y - m - 60) / rows
    r = min(cw, rh) * 0.4
    for i, a in enumerate(amounts):
        rr, cc = divmod(i, cols)
        cx, cy = m + cw * (cc + 0.5), y - rh * (rr + 0.5)
        doc.circle(cx, cy, r, stroke=[t["primary"], t["secondary"], t["accent"]][i % 3], width=1.6)
        doc.text(cx, cy - 6, f"${a}", "Display", 16, t["ink"], "center")
    doc.text(w / 2, m + 24, "50 circles  ·  $1,000 total", "WorkSans-Bold", 12, t["primary"], "center")


def p_debt_payoff(doc, page):
    w, m = doc.w, doc.m
    y = doc.header(page.get("title", "Debt Payoff Plan"), "List debts smallest to largest, or highest rate first", size=28)
    full = w - 2 * m
    y = section_title(doc, m, y, "My debts")
    y = table(doc, m, y, [full * 0.06, full * 0.34, full * 0.2, full * 0.12, full * 0.18, full * 0.1], 21,
              ["#", "Debt", "Balance", "Rate", "Min. pay", "Done"], 8, first_col=[str(i) for i in range(1, 9)], check_col=5) - 20
    y = section_title(doc, m, y, "Payment log")
    rows = int((y - m - 10) // 21) - 1
    table(doc, m, y, [full * 0.18, full * 0.34, full * 0.24, full * 0.24], 21, ["Date", "Debt", "Paid", "New balance"], rows)


def p_expense_log(doc, page):
    w, m = doc.w, doc.m
    y = doc.header(page.get("title", "Expense Log"), size=28)
    write_line(doc, m, y - 6, "Month:", w / 2 - m)
    y -= 26
    full = w - 2 * m
    rows = int((y - m - 10) // 21) - 1
    table(doc, m, y, [full * 0.14, full * 0.44, full * 0.24, full * 0.18], 21, ["Date", "Description", "Category", "Amount"], rows)


def p_year_overview(doc, page):
    t, w, m = doc.t, doc.w, doc.m
    y = doc.header(page.get("title", "Year at a Glance"), size=28)
    write_line(doc, w / 2 - 70, y - 6, "Year:", 140)
    y -= 26
    cols, rows, gap = 3, 4, 10
    cw = (w - 2 * m - gap * 2) / cols
    ch = (y - m - gap * 3) / rows
    full_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                   "October", "November", "December"]
    for k, mon in enumerate(full_months):
        r, c = divmod(k, cols)
        x, ytop = m + c * (cw + gap), y - r * (ch + gap)
        doc.rect(x, ytop - ch, cw, ch, stroke=t["accent"], width=1, radius=10)
        doc.rect(x, ytop - 26, cw, 26, fill=t["primary"] if k % 2 == 0 else t["secondary"], radius=10)
        doc.rect(x, ytop - 26, cw, 10, fill=t["primary"] if k % 2 == 0 else t["secondary"])
        doc.text(x + cw / 2, ytop - 18, mon, "WorkSans-Bold", 11.5, "#FFFFFF", "center")
        step = (ch - 36) / 4
        for i, lab in enumerate(["Income", "Spent", "Saved", "Debt paid"]):
            yy = ytop - 30 - step * (i + 0.7)
            doc.text(x + 10, yy, lab, "WorkSans-Regular", 9.5, t["ink"])
            doc.line(x + 66, yy - 2, x + cw - 10, yy - 2, t["muted"], 0.5)


def p_weekly_meals(doc, page):
    t, w, m = doc.t, doc.w, doc.m
    y = doc.header(page.get("title", "Weekly Meal Planner"), size=28)
    write_line(doc, m, y - 6, "Week of:", w / 2 - m)
    y -= 26
    full = w - 2 * m
    meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    first = full * 0.15
    mw = (full - first) / 4
    row_h = (y - m - 150) / 8
    bottom = table(doc, m, y, [first] + [mw] * 4, row_h, ["Day"] + meals, 7, first_col=DAYS, size=11)
    y = bottom - 16
    half = (full - 16) / 2
    for k, lab in enumerate(["Prep ahead", "Don't forget to buy"]):
        x = m + k * (half + 16)
        doc.rect(x, m + 6, half, y - m - 6, fill=t["tint"], radius=10)
        doc.text(x + 12, y - 18, lab.upper(), "WorkSans-Bold", 10.5, t["secondary"])
        for i in range(int((y - m - 40) // 20)):
            doc.line(x + 12, y - 40 - i * 20, x + half - 12, y - 40 - i * 20, t["muted"], 0.5)


def p_grocery_list(doc, page):
    t, w, m = doc.t, doc.w, doc.m
    y = doc.header(page.get("title", "Grocery List"), size=28)
    cats = page.get("categories", ["Produce", "Dairy & Eggs", "Meat & Seafood", "Bakery", "Pantry", "Frozen",
                                   "Snacks", "Drinks", "Household", "Other"])
    cols, gap = 2, 14
    rows = -(-len(cats) // cols)
    cw = (w - 2 * m - gap) / cols
    ch = (y - m - gap * (rows - 1)) / rows
    for k, cat in enumerate(cats):
        r, c = divmod(k, cols)
        x, ytop = m + c * (cw + gap), y - r * (ch + gap)
        doc.rect(x, ytop - ch, cw, ch, stroke=t["accent"], width=1, radius=10)
        doc.text(x + 12, ytop - 18, cat.upper(), "WorkSans-Bold", 10.5, [t["primary"], t["secondary"]][k % 2])
        n = int((ch - 30) // 19)
        for i in range(n):
            yy = ytop - 34 - i * 19
            doc.checkbox(x + 12, yy, 9, t["muted"])
            doc.line(x + 27, yy, x + cw - 12, yy, t["muted"], 0.5)


def p_recipe_cards(doc, page):
    t, w, h, m = doc.t, doc.w, doc.h, doc.m
    gap = 18
    ch = (h - 2 * m - gap) / 2
    for k in range(2):
        ytop = h - m - k * (ch + gap)
        x, cw = m, w - 2 * m
        doc.rect(x, ytop - ch, cw, ch, stroke=t["primary"], width=1.4, radius=12)
        doc.rect(x + 1, ytop - 40, cw - 2, 39, fill=t["tint"], radius=12)
        doc.text(x + 16, ytop - 26, "Recipe:", "Display", 17, t["primary"])
        doc.line(x + 90, ytop - 28, x + cw - 16, ytop - 28, t["muted"], 0.7)
        yy = ytop - 62
        for i, lab in enumerate(["Serves:", "Prep:", "Cook:", "From:"]):
            write_line(doc, x + 16 + i * (cw - 32) / 4, yy, lab, (cw - 32) / 4 - 12)
        left = (cw - 48) * 0.4
        doc.text(x + 16, yy - 26, "INGREDIENTS", "WorkSans-Bold", 10, t["secondary"])
        doc.text(x + 32 + left, yy - 26, "DIRECTIONS", "WorkSans-Bold", 10, t["secondary"])
        n = int((yy - 40 - (ytop - ch)) // 19)
        for i in range(n):
            ly = yy - 44 - i * 19
            doc.line(x + 16, ly, x + 16 + left, ly, t["muted"], 0.5)
            doc.line(x + 32 + left, ly, x + cw - 16, ly, t["muted"], 0.5)
        doc.line(x + 24 + left, yy - 34, x + 24 + left, ytop - ch + 14, t["accent"], 0.8)


def p_pantry(doc, page):
    w, m = doc.w, doc.m
    y = doc.header(page.get("title", "Pantry Inventory"), "Check what you have before you shop", size=28)
    full = (w - 2 * m - 14) / 2
    rows = int((y - m - 10) // 21) - 1
    for k in range(2):
        table(doc, m + k * (full + 14), y, [full * 0.6, full * 0.2, full * 0.2], 21, ["Item", "Qty", "Buy"], rows, check_col=2)


def p_month_meals(doc, page):
    t, w, m = doc.t, doc.w, doc.m
    y = doc.header(page.get("title", "Monthly Dinner Plan"), size=28)
    write_line(doc, w / 2 - 90, y - 6, "Month:", 180)
    y -= 24
    cw = (w - 2 * m) / 7
    doc.rect(m, y - 22, w - 2 * m, 22, fill=t["primary"])
    for i, d in enumerate(DAYS):
        doc.text(m + cw * (i + 0.5), y - 15, d[:3].upper(), "WorkSans-Bold", 10, "#FFFFFF", "center")
    rh = (y - 22 - m) / 5
    for r in range(5):
        for c in range(7):
            x, yy = m + c * cw, y - 22 - (r + 1) * rh
            doc.rect(x, yy, cw, rh, stroke=t["muted"], width=0.5, fill=t["tint"] if (r + c) % 2 == 0 else None)
            doc.rect(x + 4, yy + rh - 18, 16, 14, stroke=t["accent"], width=0.6, radius=3)


def p_meal_ideas(doc, page):
    t, w, m = doc.t, doc.w, doc.m
    y = doc.header(page.get("title", "Family Favorites"), "Meals everyone loves, for busy weeks", size=28)
    cats = ["Breakfast", "Lunch", "Dinner", "Snacks & Treats"]
    gap = 14
    cw = (w - 2 * m - gap) / 2
    ch = (y - m - gap) / 2
    for k, cat in enumerate(cats):
        r, c = divmod(k, 2)
        x, ytop = m + c * (cw + gap), y - r * (ch + gap)
        doc.rect(x, ytop - ch, cw, ch, stroke=t["accent"], width=1, radius=10)
        doc.ornament(x + 18, ytop - 18, 7, t["secondary"])
        doc.text(x + 32, ytop - 23, cat, "Display", 15, t["primary"])
        for i in range(int((ch - 44) // 21)):
            doc.line(x + 14, ytop - 48 - i * 21, x + cw - 14, ytop - 48 - i * 21, t["muted"], 0.5)


PAGE_KINDS = {
    "monthly_budget": p_monthly_budget, "bill_tracker": p_bill_tracker, "sinking_funds": p_sinking_funds,
    "savings_challenge": p_savings_challenge, "debt_payoff": p_debt_payoff, "expense_log": p_expense_log,
    "year_overview": p_year_overview, "weekly_meals": p_weekly_meals, "grocery_list": p_grocery_list,
    "recipe_cards": p_recipe_cards, "pantry": p_pantry, "month_meals": p_month_meals, "meal_ideas": p_meal_ideas,
}


def render_planner(doc, spec, _built=None):
    doc.cover(spec["cover_lines"], spec["subtitle"], spec["badges"])
    for page in spec["content"]["pages"]:
        doc.new_page()
        PAGE_KINDS[page["kind"]](doc, page)
    closing_page(doc, spec)
