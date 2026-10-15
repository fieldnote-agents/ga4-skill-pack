# GA4 Monthly Report – free Agent Skill

Your monthly GA4 report in 10 minutes. A skill for Claude, Cursor and other Agent Skills-compatible assistants, plus a plain prompt for ChatGPT.

## Contents
- `SKILL.md` – the skill (steps, checks, missing-data rules, client-ready template)
- `references/` – CSV format, metric definitions, insight patterns, how to export from GA4
- `scripts/ga4_report.py` – CSV → markdown report (Python 3, no dependencies)
- `prompts/chatgpt-prompt.md` – version for ChatGPT / any LLM
- `sample-data/` – **fictional SAMPLE data** and its generated report

## Install
Copy this folder into your assistant's skills folder (e.g. `~/.claude/skills/ga4-monthly-report/`), or upload it where your tool accepts skills.

## Try it
```
python scripts/ga4_report.py sample-data/SAMPLE-ga4-export.csv --month 2026-09 --client "Sample Shop"
```
To practise with real-looking data, add Google's public GA4 demo account and export (see `references/export-from-ga4.md`).

Sample data is made up. Not affiliated with Google. "Google Analytics" is a trademark of Google LLC. MIT licensed.
