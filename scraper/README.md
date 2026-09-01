# The Polite Scraper

FlyRank Internship — Backend Track — Week 5 — Assignment A5

A small, polite scraping pipeline that extracts the first 3 catalogue pages of Books to Scrape.

## Target Classification
- **Target Site**: [Books to Scrape](https://books.toscrape.com/)
- **Appropriateness**: It is a practice sandbox site specifically intended for scraping practice.
- **Exact Scope**: First 3 catalogue pages only.
- **Data Collected**: Book title, product URL, price, availability, rating, and description.
- **Why this is appropriate**: The sandbox is designed to teach web scraping without burdening real production servers.
- **robots.txt result**: no robots file found

I will not reuse this code on another site without checking its rules and terms first.

## Tech Stack
- Python 3.10+
- Requests
- BeautifulSoup
- Pydantic
- JSON
- Git/GitHub

## Installation
```bash
cd scraper
python -m venv .venv

# On Unix-like:
source .venv/bin/activate
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Run Command
```bash
python src/main.py
```

## Output Files
- `output/books.json`: Contains exactly 60 valid, normalized book records.
- `output/errors.json`: Contains records that failed Pydantic validation.
- `output/run-report.json`: Contains execution metrics like start time, duration, and page counts.

## Record Schema
| Field             | Type            | Description                              |
| ----------------- | --------------- | ---------------------------------------- |
| title             | string          | Book title                               |
| product_url       | string          | Absolute canonical product URL           |
| price_text        | string          | Original displayed price                 |
| price_gbp         | number          | Normalized GBP price                     |
| availability_text | string          | Original availability text               |
| rating_text       | string          | Original rating text                     |
| description       | string/null     | Book description                         |
| source_page       | string          | Catalogue page where book was discovered |
| fetched_at        | string/datetime | Fetch timestamp                          |

## Politeness Rules
- **Identifying User-Agent**: Includes a repository link so the owner knows who is scraping.
- **Timeout**: Set to 10 seconds to avoid hanging indefinitely.
- **HTTP Status Check**: Responses are only parsed if status is 200 OK.
- **Rate Limiting**: At least 500 ms delay between real requests to avoid hammering the server.
- **Cache Usage**: Cached pages do not trigger network requests during development.
- **Retry Logic**: Only one retry is allowed for timeout/5xx. 403 and 404 responses are not retried.
- **No Browser Automation**: Only standard HTTP requests are used.
- **Restricted Target**: Only the Books to Scrape practice sandbox is targeted.

## Caching
First request -> save HTML to cache
Later development runs -> read cache

Cache files are stored in `cache/` and are ignored by Git to avoid bloat.

## Validation
Every raw record is validated against a strict Pydantic schema before storage. Invalid records go to `errors.json` and are excluded from `books.json`.

## Idempotency
Rerunning the scraper does not create duplicate records. The final output remains exactly 60 unique books, de-duplicated by the canonical `product_url`.

## Failure Handling
One broken page is logged, skipped, and reflected in `run-report.json`, but does not crash the entire run. This failure mechanism is tested using a deliberately fake URL rather than abusing the live website.

## Run Report
Example `run-report.json`:
```json
{
  "start_time": "2026-09-02T01:50:00Z",
  "duration_seconds": 35.12,
  "pages_fetched": 63,
  "cache_hits": 0,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1
}
```

## Honest Limitation
The scraper is intentionally designed for the fixed Books to Scrape HTML structure and this assignment's three-page scope; changes to the site's HTML selectors could require maintenance.

## Ethics Note
Web scraping must be done ethically. Always use an official API when one exists, never bypass logins, paywalls, or blocks, and collect only what is needed. Check the target site's rules before reuse.

## Why No Browser?
The core assignment does not need a browser because the required data is already present in the HTML returned by the server; using a browser would add unnecessary cost.
