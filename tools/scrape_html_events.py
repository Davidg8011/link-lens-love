import urllib.request
import json
import ssl
import os
from datetime import datetime, timezone

def scrape_html(url, name):
    print(f"Scraping {url}...")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    })
    
    try:
        response = urllib.request.urlopen(req, context=ctx, timeout=10)
        if response.status == 200:
            html_content = response.read().decode('utf-8', errors='replace')
            
            return {
                "source_url": url,
                "source_type": "local_posting",
                "raw_text": html_content,
                "scraped_at": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        print(f"Error scraping {name}: {e}")
        
    return None

if __name__ == "__main__":
    urls = [
        ("https://tahoesouth.com/events/", "Tahoe_South"),
        ("https://visitlaketahoe.com/events/", "Visit_Lake_Tahoe")
    ]
    
    results = []
    for url, name in urls:
        res = scrape_html(url, name)
        if res:
            results.append(res)
            
    os.makedirs(".tmp", exist_ok=True)
    out_path = os.path.join(".tmp", "html_raw.json")
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"✅ Saved {len(results)} HTML pages matching gemini.md schema to {out_path}")
