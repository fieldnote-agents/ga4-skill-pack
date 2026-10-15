---
name: ga4-monthly-report
description: Builds a client-ready monthly Google Analytics 4 (GA4) report from a GA4 CSV export or pasted numbers. Use when the user asks for a monthly GA4 report, traffic summary, month-over-month analytics comparison, or a client analytics recap.
license: MIT
---

# GA4 Monthly Report

Turn a GA4 export into a short, accurate, client-ready monthly report.

## Inputs
- Preferred: a CSV with columns `date, channel, sessions, users, new_users, engaged_sessions, conversions, revenue` covering the current AND previous month. See `references/csv-format.md`.
- Also accepted: numbers pasted in chat, or a GA4 Explore/Reports export (map columns using `references/csv-format.md`).
- Ask for: client/site name, report month, and main goal (leads, sales, awareness) if not given.

## Steps
1. **Confirm scope.** Report month, comparison period (previous month by default; year-over-year if the user asks), property name.
2. **Load data.** If a CSV is available and you can run code, run:
   `python scripts/ga4_report.py <file.csv> --month YYYY-MM --client "Name"`
   Otherwise compute totals manually from the data.
3. **Compute KPIs** for both periods: sessions, users, new users, engagement rate (engaged_sessions / sessions), conversions, conversion rate (conversions / sessions), revenue. Definitions: `references/metrics.md`.
4. **Compare.** Absolute and % change per KPI; per-channel sessions and conversions; top 3 channel movers.
5. **Interpret.** Write 3–5 insights. Each insight states a number, a likely cause framed as a hypothesis, and an action. Use `references/insight-patterns.md`.
6. **Write the report** using the template below.
7. **Run the checks** before delivering.

## Checks (must all pass)
- [ ] Totals equal the sum of channel rows.
- [ ] Every % change uses (current − previous) / previous; shows "n/a" when previous is 0.
- [ ] Rates are between 0% and 100%.
- [ ] Report month has the expected number of days of data; flag partial months.
- [ ] No number appears in the summary that is not in the data.
- [ ] Causes are worded as hypotheses ("likely", "may"), never as facts.
- [ ] No personal data (emails, names, user IDs) in the report.

## When data is missing
- **Previous month missing:** report current values only, write "No comparison available", do not invent trends.
- **Column missing** (e.g. revenue): omit that KPI and add a line under "Data notes".
- **Partial month** (fewer days than the month): label as partial and compare daily averages instead of totals.
- **Zero/tiny volumes** (<100 sessions): avoid % changes; describe absolute numbers.
- **Sampling or thresholding warnings** in GA4: mention in "Data notes".
- **No data at all:** ask the user for an export; explain how in `references/export-from-ga4.md`. Never fabricate numbers.

## Client-ready summary template

```
# {Client} – Website performance, {Month YYYY}

## Headline
{One sentence: the most important change and what it means for the goal.}

## Key numbers
| Metric | {Month} | Previous | Change |
|---|---|---|---|
| Sessions | ... | ... | ...% |
| Users | ... | ... | ...% |
| Engagement rate | ...% | ...% | ... pp |
| Conversions | ... | ... | ...% |
| Conversion rate | ...% | ...% | ... pp |
| Revenue | ... | ... | ...% |

## What happened
- {Insight 1: number → likely cause → action}
- {Insight 2}
- {Insight 3}

## Channels
| Channel | Sessions | Change | Conversions | Change |
|---|---|---|---|---|

## Next month we recommend
1. {Action}
2. {Action}

## Data notes
{Partial data, missing columns, sampling, tracking changes.}
```

Keep the report under one page. Plain language, no jargon without explanation.
