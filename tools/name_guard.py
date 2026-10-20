"""Studio / film / anime / artist name guard (shared/RULES.md section 12a).

No such name may appear in prompts, file names or YouTube metadata. The blocked names are kept here only as
SHA-256 hashes (first 16 hex chars of the lower-case term), so the repo itself never contains them.

    python tools/name_guard.py <file or folder> ...   # exit 1 if a blocked name is found
    from name_guard import find_names; hits = find_names(text)

To add a name: python -c "import hashlib;print(hashlib.sha256('<name in lower case>'.encode()).hexdigest()[:16])"
and add the hash to BLOCKED (never the name itself).
"""
import hashlib
import re
import sys
from pathlib import Path

BLOCKED = set(['1476a7ba6b55db37', '1542ab0048c80ebc', '17bb020545950959', '199394a9966465a6', '1b12f1035dd67625', '2b7c5a18304e2f45', '2d8687bc61d5cee0', '34a533dfd7273a9b', '43999461d22f6784', '44de3ed43a38bbf7', '591f22426d2242ca', '61ed61a5ac911e60', '652d06b41ad614b1', '76cc170ea8843eff', '77392ec897b5f94d', '82e0c20020e450d4', '846f6a76ffc11155', '888da5db853449ff', '8915b42c6e098c59', '89e2e1e094c060d7', '8a1718ee736f769f', '8b78a2d5a1e36c12', '91f4be5bca5af627', '980f89cbce241a9d', '9a1aca66cd5f377c', '9fcb137736acc0c0', 'a0ee52f28507ec56', 'a4d48c365795cf4f', 'aa5052b079795627', 'b2b3a71381655464', 'b5bd06568325138c', 'b7a4300662c36f6c', 'b8ecf29a1496c55f', 'be6d7e3c5e9afaaa', 'c065043fcf4655e9', 'c34f5bd3ef8dfce3', 'c652649297eb6abd', 'c74d5ba5d94c8bd5', 'c8af2dcc8a9a9c4c', 'c9e9b67540b34192', 'cb094c1f669c96b0', 'd13ef6759c0ee25d', 'd3917655702c2801', 'd4deb5eaf6814c35', 'd7599da11d2e3176', 'd89a782082de317a', 'e6fe96f0c6ff73ed', 'e713931f60b4de0f', 'e7dcd96d934cb3cd', 'eaa2bded32cc585d', 'eb46b29c809c6ffa', 'ee85835dfdcdd572', 'f7d7cdf500d811d2'])
TEXT_EXT = {".json", ".md", ".txt", ".srt", ".py", ".ass", ".csv"}


def _h(term: str) -> str:
    return hashlib.sha256(term.encode()).hexdigest()[:16]


def find_names(text: str) -> list[str]:
    """Blocked terms (1-4 word phrases, lower case, apostrophes kept) found in text."""
    words = re.findall(r"[a-z0-9']+", text.lower())
    hits = []
    for n in range(1, 5):
        for i in range(len(words) - n + 1):
            term = " ".join(words[i:i + n])
            if _h(term) in BLOCKED:
                hits.append(term)
    return sorted(set(hits))


def scan(paths) -> dict:
    found = {}
    for p in map(Path, paths):
        files = [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else [p]
        for f in files:
            hits = find_names(f.name.replace("_", " ").replace("-", " "))
            if f.suffix.lower() in TEXT_EXT:
                hits += find_names(f.read_text(encoding="utf-8", errors="ignore"))
            if hits:
                found[str(f)] = sorted(set(hits))
    return found


if __name__ == "__main__":
    res = scan(sys.argv[1:])
    for f, hits in res.items():
        print(f"BLOCK (RULES 12a): {f}: {len(hits)} blocked name(s)")
    print("name guard: OK" if not res else "name guard: BLOCKED")
    sys.exit(1 if res else 0)
