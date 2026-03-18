import urllib.request
import json
import ssl
import os
from datetime import datetime, timezone

def scrape_reddit(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=15"
    print(f"Scraping {url}...")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    try:
        response = urllib.request.urlopen(req, context=ctx, timeout=10)
        if response.status == 200:
            data = json.loads(response.read().decode('utf-8'))
            results = []
            
            for child in data.get('data', {}).get('children', []):
                post = child.get('data', {})
                raw_text = post.get('title', '') + "\n\n" + post.get('selftext', '')
                post_url = "https://www.reddit.com" + post.get('permalink', '')
                
                results.append({
                    "source_url": post_url,
                    "source_type": "reddit",
                    "raw_text": raw_text.strip(),
                    "scraped_at": datetime.now(timezone.utc).isoformat()
                })
            
            return results
    except Exception as e:
        print(f"Error scraping {subreddit}: {e}")
    
    return []

if __name__ == "__main__":
    tahoe_posts = scrape_reddit("tahoe")
    south_tahoe_posts = scrape_reddit("southlaketahoe")
    
    all_posts = tahoe_posts + south_tahoe_posts
    
    os.makedirs(".tmp", exist_ok=True)
    out_path = os.path.join(".tmp", "reddit_raw.json")
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2)
        
    print(f"✅ Saved {len(all_posts)} reddit posts matching gemini.md schema to {out_path}")
