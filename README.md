# GA4 Skill Pack – free Agent Skills by Fieldnote Agents

Agent Skills for Google Analytics 4 reporting. Works with Claude Code, Cursor and other Agent Skills-compatible agents.

## Skills
- `skills/ga4-monthly-report` – turns a GA4 CSV export (or pasted numbers) into a client-ready monthly report with month-over-month comparison, checks and insights. Includes a stdlib-only Python script and fictional sample data.

## Install
```
npx skills add fieldnote-agents/ga4-skill-pack
```
Or copy `skills/ga4-monthly-report/` into your agent's skills folder (e.g. `~/.claude/skills/`).

## Try it
```
python skills/ga4-monthly-report/scripts/ga4_report.py skills/ga4-monthly-report/sample-data/SAMPLE-ga4-export.csv --month 2026-09 --client "Sample Shop"
```

More from Fieldnote Agents: [company-check-mcp](https://github.com/fieldnote-agents/company-check-mcp) · [EU company registers directory](https://fieldnote-agents.github.io/eu-company-registers/) (free, open source).

Contact: fieldnoteagents@mail.grokbot.com

Sample data is fictional. Not affiliated with or endorsed by Google. "Google Analytics" is a trademark of Google LLC. MIT licensed.
