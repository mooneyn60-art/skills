#!/usr/bin/env python3
"""Ask AI answer engines the questions customers ask about a business, and
save every raw answer with a timestamp.

Usage:
  python ask_ai.py --slug viridian-bookshop-willoughby            # all available API providers
  python ask_ai.py --slug X --providers gemini,serpapi            # a subset
  python ask_ai.py --slug X --print-queries                       # queries for claude-websearch mode
  python ask_ai.py --slug X --import answers.json                 # merge answers recorded by a Claude session
  python ask_ai.py --list-providers

Providers (each is skipped cleanly, with the reason logged, if its key is missing):
  serpapi          Google AI Overview via SerpApi            env SERPAPI_KEY
  gemini           Gemini API with Google Search grounding   env GEMINI_API_KEY  (GEMINI_MODEL)
  openai           OpenAI Responses API with web search      env OPENAI_API_KEY  (OPENAI_MODEL)
  claude-websearch A Claude session runs each query with its WebSearch tool and
                   records the synthesized answer verbatim (no key; see
                   routines/RUN.md). Imported with --import.

Output: answers/<slug>/<YYYY-MM-DD>.json  (runs on the same day are merged)

Import format (list of objects; only query/text are required):
  [{"provider": "claude-websearch", "question_id": "hours", "query": "...",
    "text": "<verbatim answer>", "citations": ["https://..."],
    "observed_at": "2026-10-15T21:40:00Z"}]
Use provider "google-ai-overview (press report)" with "evidence_url" and
"observed_at" set to the article date to log errors documented by journalists.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse

from common import ANSWERS_DIR, TRUTH_DIR, fetch, load_json, now_iso, save_json, today

QUESTIONS = [
    ("status", "status", "Is {name} in {town} open?"),
    ("hours", "hours", "{name} {town} hours"),
    ("deals", "offers", "{name} {town} deals specials"),
    ("legit", "legal", "Is {name} in {town} legit? Any lawsuits?"),
    ("phone", "phone", "{name} {town} phone number"),
    ("address", "address", "{name} {town} address"),
]
FIELD_OF = {qid: field for qid, field, _ in QUESTIONS}
TIMEOUT = 90


def build_queries(truth: dict) -> list[dict]:
    name = truth["name"]
    town = f'{truth["town"]} {truth.get("region", "")}'.strip()
    if truth["town"].lower() in name.lower():  # "Stefanina's Wentzville" already names the town
        town = truth.get("region", "")
    return [{"question_id": qid, "field": field,
             "query": " ".join(tpl.format(name=name, town=town).replace(" in ?", "?").split())}
            for qid, field, tpl in QUESTIONS]


# --------------------------------------------------------------- providers
class Provider:
    name = "base"
    label = "base"
    env = ""

    def missing(self) -> str | None:
        return None if os.environ.get(self.env) else f"{self.env} not set"

    def ask(self, query: str, truth: dict) -> dict:  # -> {text, citations, raw}
        raise NotImplementedError


class SerpApiAIOverview(Provider):
    """Google Search result page AI Overview, located in the business's town."""
    name, label, env = "serpapi", "Google AI Overview (via SerpApi)", "SERPAPI_KEY"

    def _get(self, params: dict) -> dict:
        params["api_key"] = os.environ[self.env]
        _, _, body = fetch("https://serpapi.com/search.json?" + urllib.parse.urlencode(params),
                           timeout=TIMEOUT)
        return json.loads(body)

    @staticmethod
    def _flatten(blocks) -> str:
        out = []
        for b in blocks or []:
            if b.get("snippet"):
                out.append(b["snippet"])
            for item in b.get("list") or []:
                t = " ".join(x for x in (item.get("title"), item.get("snippet")) if x)
                if t:
                    out.append("- " + t)
            if b.get("text_blocks"):
                out.append(SerpApiAIOverview._flatten(b["text_blocks"]))
        return "\n".join(x for x in out if x)

    def ask(self, query, truth):
        loc = f'{truth["town"]}, {truth.get("region", "")}, United States'.replace(", ,", ",")
        res = self._get({"engine": "google", "q": query, "location": loc, "hl": "en", "gl": "us"})
        aio = res.get("ai_overview") or {}
        if aio.get("page_token") and not aio.get("text_blocks"):
            aio = self._get({"engine": "google_ai_overview", "page_token": aio["page_token"]}
                            ).get("ai_overview") or {}
        text = self._flatten(aio.get("text_blocks"))
        cites = [r.get("link") for r in aio.get("references") or [] if r.get("link")]
        kg = res.get("knowledge_graph") or {}
        extra = {k: kg.get(k) for k in ("title", "address", "phone", "hours", "type") if kg.get(k)}
        return {"text": text or None, "citations": cites,
                "note": None if text else "Google showed no AI Overview for this query.",
                "raw": {"knowledge_panel": extra, "search_url": res.get("search_metadata", {}).get("google_url")}}


class GeminiGrounded(Provider):
    name, label, env = "gemini", "Gemini (Google Search grounding)", "GEMINI_API_KEY"

    def ask(self, query, truth):
        model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        payload = {"contents": [{"role": "user", "parts": [{"text": query}]}],
                   "tools": [{"google_search": {}}]}
        _, _, body = fetch(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            data=json.dumps(payload).encode(), timeout=TIMEOUT,
            headers={"Content-Type": "application/json", "x-goog-api-key": os.environ[self.env]})
        res = json.loads(body)
        cand = (res.get("candidates") or [{}])[0]
        text = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
        chunks = cand.get("groundingMetadata", {}).get("groundingChunks", [])
        cites = [c["web"]["uri"] for c in chunks if c.get("web", {}).get("uri")]
        return {"text": text or None, "citations": cites, "raw": {"model": model}}


class OpenAIWeb(Provider):
    name, label, env = "openai", "ChatGPT (OpenAI web search)", "OPENAI_API_KEY"

    def ask(self, query, truth):
        model = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
        payload = {"model": model, "input": query,
                   "tools": [{"type": os.environ.get("OPENAI_SEARCH_TOOL", "web_search"),
                              "user_location": {"type": "approximate", "country": "US",
                                                "city": truth["town"], "region": truth.get("region", "")}}]}
        _, _, body = fetch("https://api.openai.com/v1/responses", data=json.dumps(payload).encode(),
                           timeout=TIMEOUT, headers={"Content-Type": "application/json",
                                                     "Authorization": f"Bearer {os.environ[self.env]}"})
        res = json.loads(body)
        text, cites = [], []
        for item in res.get("output", []):
            for c in item.get("content", []) or []:
                if c.get("type") == "output_text":
                    text.append(c.get("text", ""))
                    cites += [a["url"] for a in c.get("annotations", []) if a.get("url")]
        return {"text": "\n".join(text) or None, "citations": list(dict.fromkeys(cites)),
                "raw": {"model": model}}


PROVIDERS = {p.name: p for p in (SerpApiAIOverview(), GeminiGrounded(), OpenAIWeb())}
LABELS = {**{p.name: p.label for p in PROVIDERS.values()},
          "claude-websearch": "Claude web search (session-run)"}


# ------------------------------------------------------------------- runs
def answers_path(slug: str, day: str | None = None):
    return ANSWERS_DIR / slug / f"{day or today()}.json"


def merge_save(slug: str, run: dict) -> str:
    path = answers_path(slug)
    doc = load_json(path, {"slug": slug, "runs": [], "answers": []})
    doc["runs"].append({k: v for k, v in run.items() if k != "answers"})
    doc["answers"] += run["answers"]
    save_json(path, doc)
    return str(path)


def run_providers(truth: dict, names: list[str]) -> dict:
    run = {"run_at": now_iso(), "location": f'{truth["town"]}, {truth.get("region", "")}',
           "providers_run": [], "providers_skipped": [], "answers": []}
    for n in names:
        p = PROVIDERS.get(n)
        if not p:
            run["providers_skipped"].append({"provider": n, "reason": "unknown provider"})
            continue
        why = p.missing()
        if why:
            run["providers_skipped"].append({"provider": n, "reason": why})
            print(f"skip {n}: {why}")
            continue
        run["providers_run"].append(n)
        for q in build_queries(truth):
            rec = {"provider": n, "engine": p.label, "mode": "api", **q, "asked_at": now_iso()}
            try:
                rec.update(p.ask(q["query"], truth))
                rec["ok"] = True
            except Exception as e:  # noqa: BLE001 - logged per question, run continues
                rec.update({"ok": False, "text": None, "citations": [], "error": str(e)[:300]})
            rec["observed_at"] = rec["asked_at"]
            run["answers"].append(rec)
            print(f"{n:8} {q['question_id']:8} {'ok' if rec['ok'] else 'ERROR'} "
                  f"{(rec.get('text') or rec.get('note') or rec.get('error') or '')[:70]!r}")
    return run


def import_answers(truth: dict, path: str, default_provider: str) -> dict:
    items = json.loads(open(path).read())
    by_query = {q["query"].lower(): q for q in build_queries(truth)}
    run = {"run_at": now_iso(), "location": f'{truth["town"]}, {truth.get("region", "")}',
           "providers_run": [], "providers_skipped": [], "answers": [], "imported_from": path}
    for it in items:
        if not it.get("text"):
            continue
        prov = it.get("provider", default_provider)
        q = by_query.get(it.get("query", "").lower(), {})
        qid = it.get("question_id") or q.get("question_id") or "other"
        rec = {"provider": prov, "engine": it.get("engine") or LABELS.get(prov, prov),
               "mode": it.get("mode") or ("press-report" if "press" in prov else "manual"),
               "question_id": qid, "field": it.get("field") or FIELD_OF.get(qid, "other"),
               "query": it.get("query"), "asked_at": it.get("asked_at") or it.get("observed_at") or now_iso(),
               "observed_at": it.get("observed_at") or now_iso(), "text": it["text"],
               "citations": it.get("citations", []), "ok": True}
        for k in ("evidence_url", "note", "screenshot", "owner_confirmed_false"):
            if it.get(k) is not None:
                rec[k] = it[k]
        run["answers"].append(rec)
        if prov not in run["providers_run"]:
            run["providers_run"].append(prov)
    return run


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug")
    ap.add_argument("--providers", default="serpapi,gemini,openai")
    ap.add_argument("--print-queries", action="store_true")
    ap.add_argument("--import", dest="imp")
    ap.add_argument("--provider", default="claude-websearch", help="default provider for --import")
    ap.add_argument("--list-providers", action="store_true")
    a = ap.parse_args()

    if a.list_providers:
        for p in PROVIDERS.values():
            print(f"{p.name:16} {p.label:40} {'ready' if not p.missing() else p.missing()}")
        print(f"{'claude-websearch':16} {LABELS['claude-websearch']:40} manual (--print-queries / --import)")
        return
    if not a.slug:
        ap.error("--slug is required")
    truth = load_json(TRUTH_DIR / f"{a.slug}.json")
    if not truth:
        sys.exit(f"No truth file for {a.slug}. Run truth.py first.")

    if a.print_queries:
        for q in build_queries(truth):
            print(f'{q["question_id"]}\t{q["query"]}')
        return
    run = import_answers(truth, a.imp, a.provider) if a.imp else \
        run_providers(truth, [x.strip() for x in a.providers.split(",") if x.strip()])
    if not run["answers"]:
        print("No answers recorded (no provider keys set?). For a keyless check use "
              "claude-websearch mode: see routines/RUN.md.")
        save_json(answers_path(a.slug).with_suffix(".skipped.json"), run)
        sys.exit(2)
    print(f"Saved {len(run['answers'])} answers -> {merge_save(a.slug, run)}")


if __name__ == "__main__":
    main()
