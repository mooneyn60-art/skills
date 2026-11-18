"""Pinterest via Make webhook. Usage: python3 src/pinterest.py boards | pins"""
import subprocess, sys, os, json
ROOT = os.path.join(os.path.dirname(__file__), "..")
HOOK = open(f"{ROOT}/.pin_hook").read().strip()  # private, git-ignored

BOARDS = {
  "santa": ("Letter to Santa Ideas", "Printable letters to Santa, replies from Santa and North Pole mail ideas for kids."),
  "kids": ("Christmas Printables for Kids", "Christmas printables, wish lists and activities for kids. Instant downloads."),
  "elf": ("Elf Arrival Ideas", "Christmas elf arrival letters, elf rules and elf welcome ideas."),
  "planner": ("2027 Planner & Budget Printables", "Minimalist printable planners, budget trackers and organization ideas for 2027."),
  "evebox": ("Christmas Eve Box Ideas", "Christmas Eve box fillers: Nice List certificates, letters from Santa and more."),
}
E = "https://www.etsy.com/listing/"
PINS = [
  ("dear-santa", "santa", "4617955241", "Letter to Santa Printable for Kids – Dear Santa Christmas Wish List", "Start a magical Christmas tradition! This printable Dear Santa letter lets kids share their name, age, nice-or-naughty status and Christmas wish list. Instant download PDF, print at home tonight. #lettertosanta #christmasprintables #dearsanta"),
  ("reply-from-santa", "santa", "4617969930", "Letter from Santa Printable – Reply from the North Pole", "Surprise your kids with a reply straight from Santa's desk! Fill in their name and what Santa is proud of, with the official Nice List checkbox. Instant download, US Letter + A4. #letterfromsanta #christmasmagic #northpole"),
  ("nice-list", "evebox", "4617970196", "Nice List Certificate Printable – Official Santa's Nice List Award", "Make it official! A printable Nice List certificate signed by Santa and the Head Elf, with a gold seal. Perfect for Christmas Eve boxes and stockings. #nicelist #christmaseveboxideas #stockingstuffers"),
  ("wish-list", "kids", "4617961559", "Christmas Wish List Printable for Kids – Dear Santa Gift List", "Help kids write (and draw!) their Christmas wishes. 5 wish lines, a draw-your-#1-wish box and a 'something nice I did' section. Instant download. #christmaswishlist #christmasactivitiesforkids"),
  ("elf-arrival", "elf", "4617961567", "Christmas Elf Arrival Letter Printable – Elf Welcome Note & Rules", "Welcome your Christmas elf with a magical arrival letter! Fill in your child's name and your elf's name, plus fun Elf Rules. Print in minutes. #elfarrival #elfideas #christmastraditions"),
  ("bundle", "kids", "4617961573", "Santa Mail Kit Printable Bundle – Letter to Santa, Reply, Nice List & Elf", "5 matching Christmas printables in one instant download: Dear Santa letter, reply from Santa, wish list, Nice List certificate and elf arrival letter. #santamail #christmasprintables #christmastraditions"),
]

PINS += [
  ("coloring", "kids", "4619864564", "Christmas Coloring Pages for Kids – 20 Printable Pages + Note from Santa", "20 printable Christmas coloring pages: Santa's toy factory, reindeer, elves, gingerbread and cozy scenes, plus a bonus Note from Santa. Perfect for Christmas Eve boxes and winter break. Instant download. #christmascoloringpages #kidsactivities #christmaseveboxideas #printables"),
  ("planner", "planner", "4617986184", "2027 Planner Printable – Minimalist Monthly, Weekly & Daily Planner", "Get organized for 2027! A calm, minimalist printable planner: year at a glance, goals, 12 dated monthly calendars, weekly & daily pages and a habit tracker. US Letter + A4, instant download. #2027planner #printableplanner #minimalistplanner #newyeargoals"),
  ("budget", "planner", "4617978275", "Budget Planner Printable – Monthly Budget, Bill & Debt Payoff Tracker", "Take control of your money in 2027 with this printable budget planner: monthly budget, expense & bill trackers, savings goals, sinking funds, debt payoff and a no-spend challenge. #budgetplanner #budgettracker #debtpayoff #savingmoney"),
]

def post(key, url, method, meta, img=None):
    a = ["curl", "-sS", "-w", " %{http_code}", HOOK, "-F", f"key={key}", "-F", f"url={url}", "-F", f"method={method}", "-F", f"meta={json.dumps(meta)}"]
    if img: a += ["-F", f"img=@{img};type=image/jpeg"]
    print(key, subprocess.run(a, capture_output=True, text=True).stdout)

if sys.argv[1] == "boards":
    only = sys.argv[2:] or list(BOARDS)
    for k, (n, d) in [(k, BOARDS[k]) for k in only]:
        post(f"board-{k}", "/v5/boards", "POST", {"name": n, "description": d, "privacy": "PUBLIC"})
elif sys.argv[1] == "pins":
    ids = json.load(open(f"{ROOT}/pins/board_ids.json"))
    which = sys.argv[2] if len(sys.argv) > 2 else "AB"
    slugs = sys.argv[3:]
    for slug, board, lid, title, desc in [x for x in PINS if not slugs or x[0] in slugs]:
        for v in which:
            post(f"pin-{slug}-{v}", "/v5/pins", "POST", {
                "board_id": ids[board], "title": title, "description": desc, "link": E + lid,
                "alt_text": title, "media_source": {"source_type": "image_base64", "content_type": "image/jpeg", "data": "__IMG__"}},
                f"{ROOT}/pins/pin-{slug}-{v}.jpg")
