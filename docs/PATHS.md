# Path rule (PC + cloud, 2026-11-06)

Repo root = `D:\my-tubes` on the PC, `/home/user/story-channel` (symlink `/home/user/my-tubes`) in the cloud. Never write an absolute path in a tracked source file.

- Python: `ROOT = Path(__file__).resolve().parent...` (like `scripts/build_deck.py`); story scripts use their own folder via `__file__`.
- `deck.json` / HTML for the deck engine: use `{ROOT}` (e.g. `<img src="{ROOT}/channels/devrobolab/stories/039_x/cut/a.png">`); `build_deck.py` replaces it with the real root (old `file:///home/user/story-channel`, `file:///D:/my-tubes`, `D:/Story-Channel` prefixes are mapped too).
- Static HTML: relative paths (`../../../../shared/fonts/...`).
- Logs (`*.log`, `parallax_log.jsonl`) and generated `build/deck.html` are history/outputs: they may contain old absolute paths, ignore them.
