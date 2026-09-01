import os
import time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/ehtisham5618/Task-CRUD-API.git)"

def fetch_and_cache(url, cache_filename):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
        
    cache_path = os.path.join(CACHE_DIR, cache_filename)
    
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content
            
    print(f"FETCH: {url}")
    headers = {'User-Agent': USER_AGENT}
    time.sleep(0.5) # 500 ms politeness delay
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
        
    if response.status_code != 200:
        print(f"Failed to fetch {url}. Status: {response.status_code}")
        return None
        
    content = response.text
    
    with open(cache_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return content

def main():
    # Stage 1 & 2: fetch catalogue pages and extract book URLs
    base_url = "https://books.toscrape.com/catalogue/page-1.html"
    current_url = base_url
    
    discovered_urls = set()
    pages_processed = 0
    
    while pages_processed < 3 and current_url:
        page_num = pages_processed + 1
        cache_file = f"catalogue-page-{page_num}.html"
        html_content = fetch_and_cache(current_url, cache_file)
        
        if not html_content:
            break
            
        pages_processed += 1
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract book links (h3 a)
        for h3 in soup.select("h3 a"):
            href = h3.get("href")
            if href:
                absolute_url = urljoin(current_url, href)
                discovered_urls.add(absolute_url)
                
        # Find next page
        next_btn = soup.select_one("li.next a")
        if next_btn and pages_processed < 3:
            next_href = next_btn.get("href")
            current_url = urljoin(current_url, next_href)
        else:
            current_url = None
            
    print(f"catalogue_pages={pages_processed}")
    print(f"discovered={len(discovered_urls)}")
    print(f"unique_urls={len(discovered_urls)}")

if __name__ == "__main__":
    main()
