# The Polite Scraper

FlyRank Internship — Backend Track — Week 5 — Assignment A5

A small, polite scraping pipeline that downloads the first 3 catalogue pages of
[Books to Scrape](https://books.toscrape.com/), discovers exactly 60 unique book
URLs, extracts and normalises every record, validates it with Pydantic, and stores
the results in JSON output files.

**Assignment Progression:**
- **Assignment 1**: In-memory CRUD API with REST fundamentals
- **Assignment 2**: SQLite persistent storage with Git integration
- **Assignment 3**: PostgreSQL database with Docker containerization
- **Assignment 4**: Supabase Auth with JWT-based protected routes
- **Assignment 5**: Polite web scraping pipeline with caching and validation

---

## Target Classification

| Property       | Detail                                                          |
| -------------- | --------------------------------------------------------------- |
| **Target site** | Books to Scrape — https://books.toscrape.com/                 |
| **Why appropriate** | Official practice sandbox built specifically for teaching web scraping. No real users, no real commerce. |
| **Scope** | First 3 catalogue pages only (pages 1–3)                       |
| **Expected books** | Exactly 60 unique titles                                    |
| **Fields collected** | Title, price, availability, rating, description, product URL |
| **robots.txt** | `no robots file found` — the server returned HTTP 404 for `https://books.toscrape.com/robots.txt` |

I will not reuse this code on another site without checking its rules and terms first.

---

## Tech Stack

- **Python** 3.10+
- **Requests** – HTTP client
- **BeautifulSoup** (bs4) – HTML parsing
- **Pydantic** – schema validation
- **JSON** (stdlib) – output serialisation
- **Git / GitHub**

---

## Installation

```bash
cd scraper
python -m venv .venv

# Unix/macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

No API keys, accounts, or paid services are required.

---

## Run Command

Normal run (all 60 books):

```bash
python src/main.py
```

Failure-resilience demonstration (adds one fake URL):

```bash
python src/main.py --test-failure
```

---

## Output Files

| File | Contents |
| ---- | -------- |
| `output/books.json` | 60 valid, normalised book records |
| `output/errors.json` | Records that failed Pydantic validation (empty on clean runs) |
| `output/run-report.json` | Execution metrics for every run |

---

## Record Schema

| Field             | Type        | Description                              |
| ----------------- | ----------- | ---------------------------------------- |
| title             | string      | Book title                               |
| product_url       | string      | Absolute canonical product URL           |
| price_text        | string      | Original displayed price (e.g. `£51.77`) |
| price_gbp         | number      | Normalised GBP price (e.g. `51.77`)      |
| availability_text | string      | Original availability text               |
| rating_text       | string      | Original rating word (e.g. `Three`)      |
| description       | string/null | Book description (`null` if absent)      |
| source_page       | string      | Catalogue page where book was discovered |
| fetched_at        | string      | ISO 8601 UTC fetch timestamp             |

---

## Politeness Rules

- **Identifying User-Agent** — includes a link to the repository so the server owner knows who is making requests.
- **Finite timeout** — all requests use a 10-second timeout; they never hang indefinitely.
- **HTTP status check** — a response is only parsed if the status code is 200 OK.
- **500 ms delay between real requests** — `time.sleep(0.5)` runs before every outgoing HTTP request.
- **Cache bypasses the network** — cached pages are read from disk with no delay and no network traffic.
- **No retry on 403/404** — a definitive refusal or missing page is logged and skipped.
- **One retry for timeout/5xx** — transient failures get a single retry after a 2-second wait, nothing more.
- **No browser automation** — plain HTTP requests only; Selenium/Playwright are not used.
- **Single target** — only the Books to Scrape practice sandbox is scraped.

---

## Caching

First request → save HTML to `cache/` on disk.  
Later runs → read from `cache/` — no network traffic, no delay, no load on the server.

```text
cache/
├── catalogue-page-1.html
├── catalogue-page-2.html
├── catalogue-page-3.html
└── books/
    ├── a-light-in-the-attic_1000.html
    └── ...
```

Cache files are listed in `.gitignore` and are not committed.

---

## Validation

Every raw record is run through a strict Pydantic `BookRecord` schema before storage:

- If validation passes → the record goes into `output/books.json`.
- If validation fails → the record (with its error message) goes into `output/errors.json`.
- Invalid records never enter `books.json`.

---

## Idempotency

Running the scraper twice does not produce 120 records.

`books.json` is regenerated each run and de-duplicated by canonical `product_url`.  
The result is always exactly 60 unique books.

---

## Failure Handling

Each book page is processed independently. If one page fails (network error, 4xx, 5xx):

- The failure is logged to the console.
- The page is skipped.
- All other pages continue normally.
- `run-report.json` records an accurate `failed_pages` count.

The failure mechanism is tested using a deliberately fake URL via `--test-failure` rather than abusing the live website.

---

## Run Report

Example `output/run-report.json` from a fully cached run:

```json
{
  "start_time": "2026-09-01T21:04:54Z",
  "duration_seconds": 0.88,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0
}
```

Example from `--test-failure` (one intentionally broken page):

```json
{
  "start_time": "2026-09-01T21:03:13Z",
  "duration_seconds": 2.85,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1
}
```

---

## Project Structure

```text
scraper/
├── src/
│   └── main.py          # Single-file pipeline (Stages 0–5)
├── cache/               # Downloaded HTML (Git-ignored)
│   ├── catalogue-page-1.html
│   ├── catalogue-page-2.html
│   ├── catalogue-page-3.html
│   └── books/           # One file per book detail page
├── output/              # Results committed as sample evidence
│   ├── books.json       # 60 valid records
│   ├── errors.json      # Validation failures
│   └── run-report.json  # Run metrics
├── README.md
├── .gitignore
└── requirements.txt
```

---

## Honest Limitation

The scraper is designed for the fixed HTML structure of Books to Scrape and the three-page scope of this assignment.
Changes to the site's CSS selectors (e.g. `p.price_color`, `p.star-rating`) would require maintenance.
It is not a general-purpose crawler.

---

## Ethics Note

Web scraping is only appropriate when done responsibly:

- Always use an official API when one exists.
- Never bypass logins, paywalls, or blocks.
- Collect only the data you actually need.
- Identify your scraper honestly in the User-Agent header.
- Check the target site's `robots.txt` and terms of service before scraping.

---

## Why No Browser?

The required data (title, price, rating, description) is present in the static HTML
returned by the server. A headless browser (Selenium, Playwright) would add significant
overhead and complexity for no benefit on this assignment's target.

---

## Author

**Ehtisham Abid**

---

**Happy coding!**
