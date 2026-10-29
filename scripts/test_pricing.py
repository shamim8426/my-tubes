"""Offline tests for actual-cost logging (no API calls, no money). Run: python -X utf8 scripts/test_pricing.py

Uses fake API responses in the shapes Gemini reports usage (interactions API and generateContent usageMetadata),
a temporary copy of cost_log.csv, and blocks requests.post so nothing can reach the network.
"""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import requests  # noqa: E402

requests.post = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("network blocked in tests"))

import cost_log  # noqa: E402
import pricing  # noqa: E402
import story_budget  # noqa: E402

IMG = "gemini-nano-banana-2.1"
TTS = "gemini-3.8-flash-tts"
R = pricing.rates(IMG)
INR = pricing.usd_to_inr()
ok = 0


def eq(a, b, what, tol=1e-9):
    global ok
    assert abs(a - b) <= tol, f"{what}: {a} != {b}"
    ok += 1
    print(f"  ok  {what}: {a:.6f}")


print("1. image, interactions-style usage split by modality (text + 3 refs in, image + thinking out)")
resp = {"outputs": [{"type": "image", "data": "AAAA"}],
        "usage": {"total_input_tokens": 4300, "total_output_tokens": 1120, "total_thought_tokens": 600,
                  "output_tokens_by_modality": [{"modality": "image", "tokens": 1120}]}}
c = pricing.image_cost(IMG, "1K", resp, prompt_chars=1200, n_refs=3)
want = 4300 / 1e6 * 1.50 + 1120 / 1e6 * 30.00 + 600 / 1e6 * 7.50
eq(c["actual_usd"], want, "actual USD")
eq(c["estimated_usd"], (1200 / 4 + 3 * 1120) / 1e6 * 1.50 + 1120 / 1e6 * 30.00, "estimate USD")
print(f"      -> actual ₹{c['actual_usd'] * INR:.2f} vs old flat ₹{0.0336 * INR:.2f}")

print("2. image, generateContent usageMetadata (no thinking split, modality details)")
resp = {"candidates": [{"content": {"parts": [{"inlineData": {"data": "AAAA"}}]}}],
        "usageMetadata": {"promptTokenCount": 2600, "candidatesTokenCount": 1290, "thoughtsTokenCount": 0,
                          "candidatesTokensDetails": [{"modality": "IMAGE", "tokenCount": 1120},
                                                      {"modality": "TEXT", "tokenCount": 170}]}}
c = pricing.image_cost(IMG, "1K", resp, prompt_chars=800, n_refs=2)
eq(c["actual_usd"], 2600 / 1e6 * 1.5 + 1120 / 1e6 * 30 + 170 / 1e6 * 7.5, "actual USD")

print("3. image, usage without modality split -> image part from the size table, rest at text rate")
resp = {"usage": {"input_tokens": 1500, "output_tokens": 1500}}
c = pricing.image_cost(IMG, "2K", resp, prompt_chars=400, n_refs=1)
eq(c["actual_usd"], 1500 / 1e6 * 1.5 + 1500 / 1e6 * 30, "2K: all 1500 output tokens <= 1680 count as image")

print("4. image, no usage in the response -> actual is None, estimate is used")
c = pricing.image_cost(IMG, "1K", {"outputs": [{"type": "image", "data": "AAAA"}]}, prompt_chars=400, n_refs=0)
assert c["actual_usd"] is None
eq(c["estimated_usd"], 100 / 1e6 * 1.5 + 1120 / 1e6 * 30, "estimate USD")

print("5. TTS usage (today's rate and the 2027 price change)")
resp = {"outputs": [{"type": "audio", "data": "AAAA"}], "usage": {"total_input_tokens": 40, "total_output_tokens": 90}}
c = pricing.tts_cost(TTS, resp, text_chars=80, seconds=3.6)
eq(c["actual_usd"], 40 / 1e6 * 0.5 + 90 / 1e6 * 9.0, "TTS actual USD")
from datetime import date  # noqa: E402
eq(pricing.rates(TTS, date(2027, 1, 2))["output_audio_per_1m"], 18.0, "2027-01-01 audio rate")

print("6. cost_log on a temp copy: migration, actual/estimate/GST columns, story total, budget STOP")
tmp = Path(tempfile.mkdtemp())
real = cost_log.LOG
cost_log.LOG = tmp / "cost_log.csv"
cost_log.USAGE_LOG = tmp / "usage_log.jsonl"
shutil.copy(real, cost_log.LOG)
n_old = len(cost_log._rows())
story = "003_mitthu-ne-sab-bata-diya"
old_line = story_budget.summary_line(story)
f = cost_log.ROOT / "channels/jugnu-stories/stories" / story / "images/scene_99_test.png"
resp = {"usage": {"total_input_tokens": 4300, "total_output_tokens": 1120, "total_thought_tokens": 600,
                  "output_tokens_by_modality": [{"modality": "image", "tokens": 1120}]}}
cost = pricing.image_cost(IMG, "1K", resp, prompt_chars=1200, n_refs=3)
row = cost_log.record_call(f, IMG, "1K", cost, usage=pricing.read_usage(resp))
rows = cost_log._rows()
assert list(rows[0].keys()) == cost_log.FIELDS and len(rows) == n_old + 1
assert rows[0]["actual_inr"] == "" and rows[0]["estimated_inr"] == rows[0]["cost_inr"], "old rows: estimate only"
eq(float(row["actual_inr"]), cost["actual_usd"] * INR, "row actual ₹", 1e-4)
eq(float(row["gst_inr"]), float(row["cost_inr"]) * 0.18, "row GST ₹", 0.006)
print("     ", cost_log.summary(row))
print("      before:", old_line)
print("      after: ", story_budget.summary_line(story))
assert cost_log.USAGE_LOG.read_text(encoding="utf-8").count("total_thought") == 0  # normalised usage stored
try:
    story_budget.check(story, 100.0)
    raise AssertionError("cap STOP expected")
except SystemExit as e:
    print("      STOP works:", str(e)[:110])
    ok += 1
cost_log.LOG = real
shutil.rmtree(tmp)
print(f"\nALL {ok} CHECKS PASSED (no network, real cost_log.csv untouched)")
