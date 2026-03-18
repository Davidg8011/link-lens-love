import urllib.request
import json
import ssl

def check_url(name, url):
    print(f"Testing connectivity to {name}...")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    })
    
    try:
        response = urllib.request.urlopen(req, context=ctx, timeout=10)
        if response.status == 200:
            print(f"✅ {name} is reachable (Status: 200).")
            # Optionally read a tiny bit just to ensure body is there
            body = response.read(100)
            if len(body) > 0:
                print(f"   Response payload contains data.")
            return True
        else:
            print(f"⚠️ {name} returned status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error for {name}: {e.code} - {e.reason}")
    except Exception as e:
        print(f"❌ Failed to reach {name}: {str(e)}")
    return False

if __name__ == "__main__":
    print("Initiating Phase 2: Link Verification...")
    sources = [
        ("Reddit SouthLakeTahoe (JSON)", "https://www.reddit.com/r/southlaketahoe.json"),
        ("Reddit Tahoe (JSON)", "https://www.reddit.com/r/tahoe.json"),
        ("Tahoe South Events", "https://tahoesouth.com/events/"),
        ("Visit Lake Tahoe Events", "https://visitlaketahoe.com/events/")
    ]
    
    success = 0
    for name, url in sources:
        if check_url(name, url):
            success += 1
        print("-" * 50)
        
    print(f"\nConnectivity check completed: {success}/{len(sources)} successful.")
