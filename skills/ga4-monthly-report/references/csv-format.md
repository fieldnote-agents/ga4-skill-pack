# CSV format

Required columns (header row, lower-case):

| column | type | notes |
|---|---|---|
| date | YYYY-MM-DD (or YYYYMMDD as GA4 exports) | one row per date+channel |
| channel | text | GA4 "Session default channel group" |
| sessions | int | |
| users | int | "Total users" — summing daily users overstates unique users; label as "user-days" if needed |
| new_users | int | optional |
| engaged_sessions | int | optional; needed for engagement rate |
| conversions | int | optional; GA4 now calls these "key events" |
| revenue | float | optional; "Total revenue" |

Common GA4 header names are mapped automatically by the script:
`Session default channel group`→channel, `Total users`→users, `New users`→new_users, `Engaged sessions`→engaged_sessions, `Key events`/`Conversions`→conversions, `Total revenue`→revenue, `Date`→date, `Sessions`→sessions.
GA4 CSV exports begin with `#` comment lines; they are skipped.
