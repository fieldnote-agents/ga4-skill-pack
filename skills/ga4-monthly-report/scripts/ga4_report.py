#!/usr/bin/env python3
"""Turn a GA4 CSV export into a monthly markdown report. Standard library only. MIT."""
import argparse, csv, io, sys
from collections import defaultdict

ALIASES = {"session default channel group": "channel", "default channel group": "channel",
           "total users": "users", "new users": "new_users", "engaged sessions": "engaged_sessions",
           "key events": "conversions", "total revenue": "revenue"}
NUM = ["sessions", "users", "new_users", "engaged_sessions", "conversions", "revenue"]

def norm(h):
    h = h.strip().lower()
    return ALIASES.get(h, h.replace(" ", "_"))

def load(path):
    with open(path, encoding="utf-8-sig") as f:
        lines = [l for l in f if l.strip() and not l.startswith("#")]
    rows = list(csv.DictReader(io.StringIO("".join(lines))))
    out, cols = [], set()
    for r in rows:
        r = {norm(k): (v or "").strip() for k, v in r.items() if k}
        cols |= set(r)
        d = r.get("date", "").replace("-", "")
        if len(d) != 8: continue
        r["month"] = f"{d[:4]}-{d[4:6]}"; r["day"] = d
        for k in NUM:
            try: r[k] = float(r.get(k, "").replace(",", "")) if r.get(k, "") != "" else 0.0
            except ValueError: r[k] = 0.0
        out.append(r)
    return out, cols

def prev_month(m):
    y, mo = map(int, m.split("-"))
    return f"{y-1}-12" if mo == 1 else f"{y}-{mo-1:02d}"

def days_in(m):
    import calendar; y, mo = map(int, m.split("-")); return calendar.monthrange(y, mo)[1]

def agg(rows):
    t = defaultdict(float); ch = defaultdict(lambda: defaultdict(float)); days = set()
    for r in rows:
        days.add(r["day"])
        for k in NUM:
            t[k] += r[k]; ch[r.get("channel") or "(not set)"][k] += r[k]
    return t, ch, len(days)

def pct(c, p):
    return "n/a" if not p else f"{(c-p)/p*100:+.1f}%"

def rate(a, b): return a / b * 100 if b else 0.0

def fmt(v, money=False):
    return f"{v:,.2f}" if money else f"{v:,.0f}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--month", help="YYYY-MM (default: latest in file)")
    ap.add_argument("--client", default="Client"); ap.add_argument("--out")
    a = ap.parse_args()
    rows, cols = load(a.csv)
    if not rows: sys.exit("No usable rows. Check the CSV has a date column (see references/csv-format.md).")
    month = a.month or max(r["month"] for r in rows); pm = prev_month(month)
    cur, cch, cd = agg([r for r in rows if r["month"] == month])
    prv, pch, pd = agg([r for r in rows if r["month"] == pm])
    notes = []
    if not cd: sys.exit(f"No data for {month}.")
    have_prev = pd > 0
    if not have_prev: notes.append(f"No data for {pm}: no comparison available.")
    if cd < days_in(month): notes.append(f"Partial month: {cd}/{days_in(month)} days of data. Compare with care.")
    if have_prev and pd < days_in(pm): notes.append(f"Previous month partial: {pd}/{days_in(pm)} days.")
    for k in ["engaged_sessions", "conversions", "revenue"]:
        if k not in cols: notes.append(f"Column '{k}' missing: related KPIs omitted.")
    if "users" in cols: notes.append("Users are summed from daily rows (user-days); unique monthly users are lower.")
    if cur["sessions"] < 100: notes.append("Low volume (<100 sessions): % changes are unreliable.")
    # checks
    for k in NUM:
        assert abs(sum(v[k] for v in cch.values()) - cur[k]) < 1e-6, "channel sum mismatch"
    L = [f"# {a.client} – Website performance, {month}", ""]
    hl_c, hl_p = cur["sessions"], prv["sessions"]
    L += ["## Headline", (f"Sessions were {fmt(hl_c)} ({pct(hl_c, hl_p)} vs {pm})" if have_prev else f"Sessions were {fmt(hl_c)}")
          + (f", with {fmt(cur['conversions'])} conversions ({pct(cur['conversions'], prv['conversions'])})." if "conversions" in cols and have_prev else "."), ""]
    L += ["## Key numbers", f"| Metric | {month} | {pm} | Change |", "|---|---|---|---|"]
    def row(name, c, p, kind="n"):
        if kind == "r": L.append(f"| {name} | {c:.1f}% | {p:.1f}% | {c-p:+.1f} pp |" if have_prev else f"| {name} | {c:.1f}% | – | – |")
        else: L.append(f"| {name} | {fmt(c, kind=='m')} | {fmt(p, kind=='m') if have_prev else '–'} | {pct(c,p) if have_prev else '–'} |")
    row("Sessions", cur["sessions"], prv["sessions"]); row("Users (user-days)", cur["users"], prv["users"])
    if "new_users" in cols: row("New users", cur["new_users"], prv["new_users"])
    if "engaged_sessions" in cols: row("Engagement rate", rate(cur["engaged_sessions"], cur["sessions"]), rate(prv["engaged_sessions"], prv["sessions"]), "r")
    if "conversions" in cols:
        row("Conversions", cur["conversions"], prv["conversions"])
        row("Conversion rate", rate(cur["conversions"], cur["sessions"]), rate(prv["conversions"], prv["sessions"]), "r")
    if "revenue" in cols: row("Revenue", cur["revenue"], prv["revenue"], "m")
    L += ["", "## Channels", "| Channel | Sessions | Change | Conversions | Change |", "|---|---|---|---|---|"]
    movers = []
    for ch, v in sorted(cch.items(), key=lambda x: -x[1]["sessions"]):
        p = pch.get(ch, defaultdict(float))
        L.append(f"| {ch} | {fmt(v['sessions'])} | {pct(v['sessions'], p['sessions']) if have_prev else '–'} | {fmt(v['conversions'])} | {pct(v['conversions'], p['conversions']) if have_prev else '–'} |")
        movers.append((v["sessions"] - p["sessions"], ch, v["sessions"], p["sessions"]))
    L += ["", "## What happened (draft – review and add likely causes)"]
    if have_prev:
        for d, ch, c, p in sorted(movers, key=lambda x: -abs(x[0]))[:3]:
            L.append(f"- {ch}: sessions {fmt(p)} → {fmt(c)} ({pct(c, p)}). Likely cause: _hypothesis_. Next: _action_.")
    else: L.append("- No comparison available.")
    L += ["", "## Next month we recommend", "1. _action_", "2. _action_", "", "## Data notes"] + [f"- {n}" for n in notes or ["None."]]
    md = "\n".join(L) + "\n"
    if a.out: open(a.out, "w").write(md)
    print(md)

if __name__ == "__main__": main()
