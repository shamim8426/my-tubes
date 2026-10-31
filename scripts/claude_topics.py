r"""Build/refresh the Short topic queue for the Claude explainer channel from the official docs index.

    .venv\Scripts\python -X utf8 scripts\claude_topics.py          # add new docs pages to topic_queue.json
    .venv\Scripts\python -X utf8 scripts\claude_topics.py --list   # show queue status

Each topic: id, title, url, summary, status (todo | scripted | built | uploaded | skipped), story (folder once made).
Source: https://code.claude.com/docs/llms.txt (official). Existing entries keep their status."""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
Q = ROOT / "channels/yellow-bot/topic_queue.json"
INDEX = "https://code.claude.com/docs/llms.txt"
# pages that make poor 40-60 s feature Shorts (admin / enterprise / platform setup / reference dumps)
SKIP = re.compile(r"enterprise|admin|managed|sso|bedrock|vertex|foundry|proxy|gateway|network|llm-gateway|legal|security-guidance|"
                  r"claude-security|data-usage|zero-data|monitoring|analytics|costs|billing|changelog|troubleshoot|github-enterprise|"
                  r"code-review-(setup|costs|troubleshooting|customize|pull)|linux|wsl|ios-simulator|slack|claude-tag|jetbrains|"
                  r"whats-new|2026-w|agent-sdk|/index|glossary|migration|self-hosted|hipaa|champion|communications|corporate|claude-platform|cloud-environments|third-party|devcontainer|sandbox-runtime|settings-reference|env-vars|iam|terminal-config", re.I)


def main():
    old = json.loads(Q.read_text(encoding="utf-8-sig")) if Q.exists() else []
    seen = {t["url"] for t in old}
    txt = urllib.request.urlopen(urllib.request.Request(INDEX, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8")
    if "--list" in sys.argv:
        from collections import Counter
        print(Counter(t["status"] for t in old), len(old))
        for t in old[:40]:
            print(t["status"], t["id"], t["title"])
        return
    new = []
    for m in re.finditer(r"- \[([^\]]+)\]\((https://code\.claude\.com/docs/en/[^)]+\.md)\):\s*(.*)", txt):
        title, url, summ = m.groups()
        slug = url.split("/docs/en/", 1)[1][:-3].replace("/", "-")
        if url in seen or SKIP.search(slug):
            continue
        seen.add(url)
        if False:
            continue
        new.append(dict(id=slug, title=title, url=url, summary=summ.strip(), status="todo", story=None))
    Q.write_text(json.dumps(old + new, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"queue: {len(old)} existing + {len(new)} new = {len(old) + len(new)}")


if __name__ == "__main__":
    main()
