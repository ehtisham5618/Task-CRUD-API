import os
import requests

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/ehtisham5618/Task-CRUD-API.git)"

def fetch_and_cache(url, cache_filename):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
        
    cache_path = os.path.join(CACHE_DIR, cache_filename)
    
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"CACHE HIT: {cache_filename} (Size: {len(content)} bytes)")
            return content
            
    print(f"FETCH: {url}")
    headers = {'User-Agent': USER_AGENT}
    
    # 10 second timeout as requested
    response = requests.get(url, headers=headers, timeout=10)
    
    # Status check
    if response.status_code != 200:
        print(f"Failed to fetch {url}. Status: {response.status_code}")
        return None
        
    content = response.text
    print(f"Size: {len(content)} bytes")
    
    with open(cache_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return content

def main():
    # Stage 1: fetch catalogue page 1
    url = "https://books.toscrape.com/catalogue/page-1.html"
    cache_file = "catalogue-page-1.html"
    
    html_content = fetch_and_cache(url, cache_file)

if __name__ == "__main__":
    main()
