"""
FlyRank Internship — Backend Track — Week 5 — Assignment A5
The Polite Scraper: extracts books from https://books.toscrape.com/ (first 3 pages).

Usage (from scraper/ directory):
    python src/main.py
    python src/main.py --test-failure   (adds one fake URL to prove resilience)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl, model_validator, field_validator

# ---------------------------------------------------------------------------
# Paths – resolved relative to the scraper/ project root (parent of src/)
# ---------------------------------------------------------------------------
SCRAPER_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(SCRAPER_ROOT, "cache")
BOOKS_CACHE_DIR = os.path.join(CACHE_DIR, "books")
OUTPUT_DIR = os.path.join(SCRAPER_ROOT, "output")

# ---------------------------------------------------------------------------
# Politeness settings
# ---------------------------------------------------------------------------
USER_AGENT = (
    "FlyRankInternship-A5/1.0 "
    "(+https://github.com/ehtisham5618/Task-CRUD-API)"
)
TIMEOUT = 10          # seconds
DELAY = 0.5           # 500 ms between real requests
RETRY_WAIT = 2        # seconds before the single retry on timeout/5xx

# ---------------------------------------------------------------------------
# Run-level counters
# ---------------------------------------------------------------------------
stats = {
    "pages_fetched": 0,
    "cache_hits": 0,
    "failed_pages": 0,
}


# ---------------------------------------------------------------------------
# Pydantic schema
# ---------------------------------------------------------------------------
class BookRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: str | None
    source_page: str
    fetched_at: str


# ---------------------------------------------------------------------------
# Fetching helpers
# ---------------------------------------------------------------------------
def _do_request(url: str) -> requests.Response | None:
    """Make a single HTTP GET with a 500 ms politeness delay."""
    time.sleep(DELAY)
    headers = {"User-Agent": USER_AGENT}
    return requests.get(url, headers=headers, timeout=TIMEOUT)


def fetch(url: str, cache_path: str) -> str | None:
    """
    Fetch a URL, caching the result.
    Returns the HTML string or None on failure.
    Hit: CACHE HIT logged.  Miss: real request with politeness delay.
    """
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as fh:
            content = fh.read()
        stats["cache_hits"] += 1
        return content

    # Not cached – make the real request
    print(f"  FETCH {url}")
    try:
        resp = _do_request(url)
    except requests.exceptions.Timeout:
        print(f"  TIMEOUT on first attempt – retrying once…")
        try:
            time.sleep(RETRY_WAIT)
            resp = _do_request(url)
        except Exception as exc:
            print(f"  Retry also failed: {exc}")
            stats["failed_pages"] += 1
            return None
    except requests.exceptions.RequestException as exc:
        print(f"  Request error: {exc}")
        stats["failed_pages"] += 1
        return None

    # Do not retry 4xx
    if resp.status_code in (403, 404):
        print(f"  {resp.status_code} – skipping (no retry)")
        stats["failed_pages"] += 1
        return None

    # Single retry for 5xx
    if resp.status_code >= 500:
        print(f"  {resp.status_code} – retrying once…")
        time.sleep(RETRY_WAIT)
        try:
            resp = _do_request(url)
        except Exception as exc:
            print(f"  Retry failed: {exc}")
            stats["failed_pages"] += 1
            return None

    if resp.status_code != 200:
        print(f"  HTTP {resp.status_code} – skipping")
        stats["failed_pages"] += 1
        return None

    content = resp.text
    stats["pages_fetched"] += 1
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return content


# ---------------------------------------------------------------------------
# Catalogue crawl (Stage 2)
# ---------------------------------------------------------------------------
def discover_book_urls() -> dict[str, str]:
    """
    Crawl catalogue pages 1-3 via 'next' links.
    Returns {absolute_book_url: source_catalogue_page}.
    Prints discovery counts.
    """
    start_url = "https://books.toscrape.com/catalogue/page-1.html"
    current_url = start_url
    pages_done = 0
    discovered: dict[str, str] = {}

    print("\n--- Stage 2: Discover catalogue pages ---")
    while pages_done < 3 and current_url:
        page_num = pages_done + 1
        cache_path = os.path.join(CACHE_DIR, f"catalogue-page-{page_num}.html")
        html = fetch(current_url, cache_path)
        if html is None:
            break
        pages_done += 1
        soup = BeautifulSoup(html, "html.parser")

        for h3 in soup.select("h3 a"):
            href = h3.get("href")
            if href:
                abs_url = urljoin(current_url, href)
                if abs_url not in discovered:
                    discovered[abs_url] = current_url

        nxt = soup.select_one("li.next a")
        if nxt and pages_done < 3:
            current_url = urljoin(current_url, nxt.get("href"))
        else:
            current_url = None

    print(f"  catalogue_pages={pages_done}")
    print(f"  discovered={len(discovered)}")
    print(f"  unique_urls={len(discovered)}")
    return discovered


# ---------------------------------------------------------------------------
# Book detail extraction (Stage 3)
# ---------------------------------------------------------------------------
def extract_raw(html: str, product_url: str, source_page: str) -> dict:
    """Extract the 8 required raw fields from a book detail page."""
    soup = BeautifulSoup(html, "html.parser")

    title_el = soup.select_one("div.product_main h1")
    title = title_el.text.strip() if title_el else ""

    price_el = soup.select_one("p.price_color")
    price_text = price_el.text.strip() if price_el else ""

    avail_el = soup.select_one("p.instock.availability")
    availability_text = " ".join(avail_el.text.split()) if avail_el else ""

    rating_el = soup.select_one("p.star-rating")
    rating_text = ""
    if rating_el:
        for cls in rating_el.get("class", []):
            if cls != "star-rating":
                rating_text = cls
                break

    description = None
    desc_header = soup.find(id="product_description")
    if desc_header:
        desc_p = desc_header.find_next_sibling("p")
        if desc_p:
            description = desc_p.text.strip()

    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at,
    }


# ---------------------------------------------------------------------------
# Normalise raw -> BookRecord (Stage 4)
# ---------------------------------------------------------------------------
def normalise(raw: dict) -> tuple[BookRecord | None, str | None]:
    """
    Convert price_text to price_gbp and validate with Pydantic.
    Returns (BookRecord, None) or (None, error_message).
    """
    try:
        price_str = (
            raw["price_text"]
            .replace("Â£", "")
            .replace("£", "")
            .strip()
        )
        price_gbp = float(price_str)
    except Exception as exc:
        return None, f"price parse error: {exc}"

    try:
        record = BookRecord(
            title=raw["title"],
            product_url=raw["product_url"],
            price_text=raw["price_text"],
            price_gbp=price_gbp,
            availability_text=raw["availability_text"],
            rating_text=raw["rating_text"],
            description=raw["description"],
            source_page=raw["source_page"],
            fetched_at=raw["fetched_at"],
        )
        return record, None
    except Exception as exc:
        return None, str(exc)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run(extra_urls: list[str] | None = None):
    start_time = datetime.now(timezone.utc)
    print(f"Start: {start_time.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(BOOKS_CACHE_DIR, exist_ok=True)

    # Stage 2 – discover book URLs
    discovered = discover_book_urls()

    # Optional: inject a fake URL to test failure handling
    if extra_urls:
        for url in extra_urls:
            discovered[url] = "https://books.toscrape.com/catalogue/page-1.html"
            print(f"  [TEST] Injected fake URL: {url}")

    # Stage 3 – visit each book page
    print(f"\n--- Stage 3: Fetch {len(discovered)} book pages ---")
    raw_records = []
    for book_url, source_page in discovered.items():
        slug = urlparse(book_url).path.strip("/").split("/")[-2]
        cache_path = os.path.join(BOOKS_CACHE_DIR, f"{slug}.html")
        html = fetch(book_url, cache_path)
        if html:
            raw_records.append(extract_raw(html, book_url, source_page))

    print(f"  detail_pages={len(raw_records)}")
    if raw_records:
        print("  Sample record (first):")
        print(json.dumps(raw_records[0], indent=4))

    # Stage 4 – normalise, validate, deduplicate
    print("\n--- Stage 4: Validate and store ---")
    valid_map: dict[str, dict] = {}   # product_url -> serialised record
    invalid_records: list[dict] = []

    for raw in raw_records:
        record, error = normalise(raw)
        if record:
            url_key = str(record.product_url)
            valid_map[url_key] = json.loads(record.model_dump_json())
        else:
            raw["error"] = error
            invalid_records.append(raw)

    final_records = list(valid_map.values())

    with open(os.path.join(OUTPUT_DIR, "books.json"), "w", encoding="utf-8") as fh:
        json.dump(final_records, fh, indent=2)
    with open(os.path.join(OUTPUT_DIR, "errors.json"), "w", encoding="utf-8") as fh:
        json.dump(invalid_records, fh, indent=2)

    print(f"  valid_records={len(final_records)}")
    print(f"  invalid_records={len(invalid_records)}")

    # Stage 5 – run report
    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()

    report = {
        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration_seconds": round(duration, 2),
        "pages_fetched": stats["pages_fetched"],
        "cache_hits": stats["cache_hits"],
        "valid_records": len(final_records),
        "invalid_records": len(invalid_records),
        "failed_pages": stats["failed_pages"],
    }
    with open(os.path.join(OUTPUT_DIR, "run-report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    print("\n--- Run report ---")
    print(json.dumps(report, indent=2))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Polite Scraper")
    parser.add_argument(
        "--test-failure",
        action="store_true",
        help="Inject one fake URL to demonstrate failure resilience.",
    )
    args = parser.parse_args()

    fake_urls = (
        ["https://books.toscrape.com/catalogue/this-book-does-not-exist_0/index.html"]
        if args.test_failure
        else None
    )
    run(extra_urls=fake_urls)
