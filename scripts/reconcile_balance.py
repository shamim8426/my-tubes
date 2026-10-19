"""Match our cost ledger with the real Google (AI Studio) credit balance (shared/pricing.json "budget").
Always use the AI Studio billing "Credit balance", never the cost chart (PDT time zone, updates late).

    python scripts/reconcile_balance.py <balance_inr>            # first time: set the checkpoint to this balance
    python scripts/reconcile_balance.py <balance_inr> --check    # later (e.g. after Long 03): compare, change nothing
    python scripts/reconcile_balance.py <balance_inr> --apply    # compare, move the checkpoint (GST setting is never changed)

How it avoids counting GST twice: Google's drop in balance since the checkpoint is compared with what we logged
since then, once WITHOUT GST and once WITH GST. Whichever is closer tells whether Google takes GST out of the
credits (budget_includes_gst true) or not (false — GST was paid on the top-up, so adding it again would double it).
"""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cost_log  # noqa: E402
import pricing  # noqa: E402


def logged_since(ts: str):
    rows = [r for r in cost_log._rows() if r["timestamp"] > ts]
    base = sum(cost_log.base_inr(r) for r in rows)
    return len(rows), base, base * (1 + pricing.gst_rate()), sum(1 for r in rows if not r.get("actual_inr"))


def main():
    bal = float(sys.argv[1])
    mode = "--apply" if "--apply" in sys.argv else "--check" if "--check" in sys.argv else "set"
    cfg = pricing.config()
    cp = cfg["budget"]["balance_checkpoint"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if mode != "set":
        if not cp.get("timestamp"):
            sys.exit("No checkpoint yet: run once without --check/--apply to set it.")
        drop = cp["inr"] - bal
        n, base, with_gst, est = logged_since(cp["timestamp"])
        print(f"Google balance: ₹{cp['inr']:.2f} ({cp['timestamp']}) -> ₹{bal:.2f} now: drop ₹{drop:.2f}")
        print(f"Our log since then: {n} calls ({est} estimate-only): ₹{base:.2f} without GST, ₹{with_gst:.2f} with GST")
        gst_in = abs(drop - with_gst) < abs(drop - base)
        best = with_gst if gst_in else base
        gap = (drop - best) / best * 100 if best else 0.0
        print(f"Closer match: {'WITH' if gst_in else 'WITHOUT'} GST -> budget_includes_gst should be {str(gst_in).lower()}"
              f" (now {str(cfg['budget_includes_gst']).lower()}); remaining gap {gap:+.1f}%"
              + ("  <- over 10%: check the price table in pricing.json" if abs(gap) > 10 else ""))
        if gst_in != cfg["budget_includes_gst"]:
            print("WARNING: the closer match disagrees with budget_includes_gst, which was proven on 2026-10-19 "
                  "(Google deducts cost + 18% GST). Not changed: tell the user and check the price table instead.")
        if mode == "--check":
            return
    cfg["budget"]["balance_checkpoint"].update({"timestamp": now, "inr": bal})
    pricing.CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"pricing.json: balance_checkpoint = ₹{bal:.2f} at {now}; budget_includes_gst = {cfg['budget_includes_gst']}")
    print(f"Ledger remaining now: ₹{cost_log.remaining():.2f}")


if __name__ == "__main__":
    main()
