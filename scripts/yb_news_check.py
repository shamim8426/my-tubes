"""Claude news watcher for the Yellow Bot channel: what is NEW since the last run (read-only network, free).

    .venv/Scripts/python -X utf8 scripts/yb_news_check.py [--commit] [--json]

Sources (all public, official):
  1. Claude Code changelog   https://code.claude.com/docs/en/changelog.md   (versions + 'Added' bullets)
  2. Claude Code docs index  https://code.claude.com/docs/llms.txt          (a NEW page = a new feature/topic)
  3. Anthropic news          https://www.anthropic.com/news                 (models, products, announcements)
  4. API release notes       https://docs.claude.com/en/release-notes/overview (new dated entries)
State: channels/yellow-bot/research/news_state.json. Without --commit nothing is written (dry check); with --commit the
state is updated so the next run only reports what is newer. The FIRST run only builds the baseline (reports the latest
version and nothing else) so it does not flood. Output: a plain-text report, or JSON with --json.
Nothing here uploads, spends money or edits the topic queue (the daily task / Sanchalak decides what to suggest)."""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "channels/yellow-bot/research/news_state.json"
QUEUE = ROOT / "channels/yellow-bot/topic_queue.json"
UA = {"User-Agent": "Mozilla/5.0 (YellowBot news check; contact: channel owner)"}
CHANGELOG = "https://code.claude.com/docs/en/changelog.md"
LLMS = "https://code.claude.com/docs/llms.txt"
NEWS = "https://www.anthropic.com/news"
RELNOTES = "https://docs.claude.com/en/release-notes/overview"
NEWS_CATEGORY_SLUGS = {"announcements", "features", "partnerships", "product", "policy", "research", "company", "economic-futures"}
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"


def get(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def vkey(v):
    return tuple(int(x) for x in v.split("."))


def parse_changelog(text):
    """[{version, date, added:[bullets], other:int}] newest first, as listed on the page."""
    out = []
    parts = re.split(r"\n\*\*(\d+\.\d+\.\d+)\*\*\s*\n", "\n" + text)
    for i in range(1, len(parts) - 1, 2):
        ver, body = parts[i], parts[i + 1]
        m = re.search(r"((?:%s) \d{1,2}, \d{4})" % MONTHS, body[:200])
        sect = re.split(r"\n\*\*(Added|Improved|Fixed|Changed|Removed|Deprecated)\*\*\s*\n", body)
        added = []
        for j in range(1, len(sect) - 1, 2):
            if sect[j] == "Added":
                added += [b.strip("* ").strip() for b in re.findall(r"^\*\s+(.+)$", sect[j + 1], re.M)]
        out.append({"version": ver, "date": m.group(1) if m else "", "added": added[:25]})
    return out


def doc_urls(text):
    return sorted(set(re.findall(r"https://code\.claude\.com/docs/en/[a-z0-9\-/]+\.md", text)))


def news_slugs(html):
    slugs = []
    for s in re.findall(r'href="/news/([a-z0-9\-]+)"', html):
        if s not in NEWS_CATEGORY_SLUGS and s not in slugs:
            slugs.append(s)
    return slugs


def rel_dates(html):
    txt = re.sub(r"<[^>]+>", " ", html)
    seen = []
    for d in re.findall(r"((?:%s) \d{1,2}(?:st|nd|rd|th)?, 20\d\d)" % MONTHS, txt):
        if d not in seen:
            seen.append(d)
    return seen[:12]


SOURCES = ROOT / "channels/yellow-bot/research/news_sources.json"


def _local(tag):
    return tag.split("}")[-1]


def parse_feed(text):
    """RSS/Atom -> [{title, link, date}] in feed order (newest first on the feeds we use)."""
    import xml.etree.ElementTree as ET
    items = []
    try:
        root = ET.fromstring(text.encode("utf-8"))
    except Exception:
        root = None
    if root is not None:
        for el in root.iter():
            if _local(el.tag) in ("item", "entry"):
                d = {"title": "", "link": "", "date": ""}
                for ch in el:
                    t = _local(ch.tag)
                    if t == "title":
                        d["title"] = (ch.text or "").strip()
                    elif t == "link":
                        d["link"] = (ch.get("href") or (ch.text or "")).strip() or d["link"]
                    elif t in ("pubDate", "published", "updated") and not d["date"]:
                        d["date"] = (ch.text or "").strip()
                if d["link"]:
                    items.append(d)
    if not items:  # malformed XML: regex fallback
        for blk in re.findall(r"<(?:item|entry)[ >].*?</(?:item|entry)>", text, re.S):
            t = re.search(r"<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", blk, re.S)
            l = re.search(r"<link[^>]*>(?:<!\[CDATA\[)?\s*(https?://[^<\s\]]+)", blk) or re.search(r'<link[^>]*href="([^"]+)"', blk)
            dt = re.search(r"<(?:pubDate|published|updated)[^>]*>(.*?)</", blk, re.S)
            if l:
                items.append({"title": (t.group(1).strip() if t else ""), "link": l.group(1).strip(), "date": (dt.group(1).strip() if dt else "")})
    return items


def html_links(html, base, prefix):
    out, seen = [], set()
    for p in re.findall(r'href="(%s[a-z0-9][a-z0-9\-_/]*)"' % re.escape(prefix), html):
        p = p.rstrip("/")
        if p in seen or p == prefix.rstrip("/") or "/category/" in p or p.endswith(("/rss", "/feed", "/tag")):
            continue
        seen.add(p)
        out.append({"title": p.rsplit("/", 1)[-1].replace("-", " "), "link": base + p, "date": ""})
    for p in re.findall(r'href="(%s%s[a-z0-9][a-z0-9\-_/]*)"' % (re.escape(base), re.escape(prefix)), html):
        p = p.rstrip("/")
        if p not in {x["link"] for x in out}:
            out.append({"title": p.rsplit("/", 1)[-1].replace("-", " "), "link": p, "date": ""})
    return out


def hn_items(src):
    import urllib.parse
    since = int(time.time()) - int(src.get("hours", 36)) * 3600
    found = {}
    for q in src.get("queries", ["AI"]):
        flt = f"points>{src.get('min_points', 150)},created_at_i>{since}"
        url = ("https://hn.algolia.com/api/v1/search_by_date?query=" + urllib.parse.quote(q) +
               "&tags=story&hitsPerPage=20&numericFilters=" + urllib.parse.quote(flt))
        for h in json.loads(get(url)).get("hits", []):
            if h.get("objectID") and h["objectID"] not in found:
                found[h["objectID"]] = {"title": f"{h.get('title', '')} ({h.get('points', 0)} pts)",
                                         "link": h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
                                         "date": h.get("created_at", ""), "points": h.get("points", 0), "id": h["objectID"]}
    return sorted(found.values(), key=lambda x: -x["points"])


def ai_sources(state, recent=0):
    """Whole-AI-field watch. Returns (report_list, new_state_part). First run of a source = baseline only."""
    cfg = json.loads(SOURCES.read_text(encoding="utf-8"))["sources"]
    seen_all = dict(state.get("ai_seen", {}))
    report = []
    for src in cfg:
        entry = {"id": src["id"], "org": src["org"], "new": [], "recent": [], "error": None, "baseline": False}
        try:
            if src["type"] == "rss":
                items = parse_feed(get(src["url"], 60))
                if not items:  # some feeds answer empty now and then: one retry
                    time.sleep(4)
                    items = parse_feed(get(src["url"], 60))
            elif src["type"] == "html_prefix":
                items = html_links(get(src["base"] + src["prefix"].rstrip("/"), 60), src["base"], src["prefix"])
            elif src["type"] == "hn":
                items = hn_items(src)
            else:
                items = []
            items = items[: src.get("limit", 20)]
            key = lambda it: it.get("id") or it["link"]
            known = set(seen_all.get(src["id"], []))
            if recent:
                entry["recent"] = items[:recent]
            if src["id"] not in seen_all:
                entry["baseline"] = True
            else:
                entry["new"] = [it for it in items if key(it) not in known]
            if items or src["id"] in seen_all:  # an empty first fetch must not become a 'baseline' (it would flood next run)
                seen_all[src["id"]] = ([key(it) for it in items] + list(known))[:200]
            else:
                entry["baseline"] = False
                entry["error"] = "empty first fetch (baseline postponed)"
        except Exception as e:
            entry["error"] = str(e)[:140]
        report.append(entry)
    return report, seen_all


def main():
    recent = 0
    if "--recent" in sys.argv:
        try:
            recent = int(sys.argv[sys.argv.index("--recent") + 1])
        except Exception:
            recent = 3
    commit = "--commit" in sys.argv
    as_json = "--json" in sys.argv
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    first = not state
    rep = {"checked_at": time.strftime("%Y-%m-%d %H:%M"), "first_run": first, "errors": []}
    new_state = dict(state)

    # 1. changelog
    try:
        cl = parse_changelog(get(CHANGELOG, 60))
        top = max((c["version"] for c in cl), key=vkey) if cl else None
        seen_max = state.get("latest_version")
        if first or not seen_max:
            new = [c for c in cl if c["version"] == top]  # baseline: report only the latest one
        else:
            new = sorted((c for c in cl if vkey(c["version"]) > vkey(seen_max)), key=lambda c: vkey(c["version"]), reverse=True)
        rep["new_versions"] = new
        rep["latest_version"] = top
        new_state["latest_version"] = top
        new_state.pop("versions", None)
    except Exception as e:
        rep["errors"].append(f"changelog: {e}")

    # 2. docs index
    try:
        urls = doc_urls(get(LLMS))
        queue_urls = set()
        try:
            queue_urls = {q.get("url") for q in json.loads(QUEUE.read_text(encoding="utf-8"))}
        except Exception:
            pass
        known_u = set(state.get("doc_urls", []))
        fresh = [u for u in urls if u not in known_u]
        rep["new_doc_pages"] = [] if first else fresh
        rep["doc_pages_not_in_queue"] = [u for u in urls if u not in queue_urls][:40]
        new_state["doc_urls"] = urls
    except Exception as e:
        rep["errors"].append(f"docs index: {e}")

    # 3. Anthropic news
    try:
        slugs = news_slugs(get(NEWS))
        known_s = set(state.get("news_slugs", []))
        rep["new_news"] = [] if first else [s for s in slugs if s not in known_s]
        rep["news_top"] = slugs[:8]
        new_state["news_slugs"] = slugs[:60]
    except Exception as e:
        rep["errors"].append(f"news: {e}")

    # 4. API release notes
    try:
        dates = rel_dates(get(RELNOTES, 60))
        known_d = set(state.get("relnote_dates", []))
        rep["new_relnote_dates"] = [] if first else [d for d in dates if d not in known_d]
        rep["relnotes_top"] = dates[:4]
        new_state["relnote_dates"] = dates
    except Exception as e:
        rep["errors"].append(f"release notes: {e}")

    # 5. whole AI field (labs, open models, dev tools, voice/image/video, press, HN)
    try:
        ai_rep, ai_seen = ai_sources(state, recent)
        rep["ai_field"] = ai_rep
        new_state["ai_seen"] = ai_seen
    except Exception as e:
        rep["errors"].append(f"ai sources: {e}")

    new_state["last_run"] = rep["checked_at"]
    if commit and not [e for e in rep["errors"] if not e.startswith("ai sources")]:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(new_state, indent=1, ensure_ascii=False), encoding="utf-8")
        rep["state_saved"] = True
    else:
        rep["state_saved"] = False

    if as_json:
        print(json.dumps(rep, indent=1, ensure_ascii=False))
        return 0
    print(f"Claude news check {rep['checked_at']} (first run: {first}; state saved: {rep['state_saved']})")
    for e in rep["errors"]:
        print("ERROR", e)
    print(f"Latest Claude Code version: {rep.get('latest_version')}")
    for c in rep.get("new_versions", []):
        print(f"NEW VERSION {c['version']} ({c['date']}): {len(c['added'])} 'Added' items")
        for b in c["added"][:8]:
            print("   +", b[:170])
    for u in rep.get("new_doc_pages", []):
        print("NEW DOC PAGE:", u)
    for s in rep.get("new_news", []):
        print("NEW ANTHROPIC NEWS: https://www.anthropic.com/news/" + s)
    for d in rep.get("new_relnote_dates", []):
        print("NEW API RELEASE NOTE DATE:", d)
    for a in rep.get("ai_field", []):
        if a["error"]:
            print(f"AI SOURCE ERROR {a['org']}: {a['error']}")
        elif a["baseline"]:
            print(f"AI BASELINE {a['org']} (first run, nothing reported)")
        for it in a["new"][:8]:
            print(f"NEW AI [{a['org']}] {it['title'][:120]} | {it['link']} | {it['date']}")
        for it in a["recent"]:
            print(f"RECENT [{a['org']}] {it['title'][:110]} | {it['link']} | {it['date']}")
    if rep.get("doc_pages_not_in_queue"):
        print(f"Docs pages not in our topic queue: {len(rep['doc_pages_not_in_queue'])} (first 5: {rep['doc_pages_not_in_queue'][:5]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
