import os
import sys
import json
import urllib.request
import urllib.error
import ssl
import subprocess

# 1. Load Environment Variables Deterministically
env_path = ".env"
env_vars = {}
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, val = line.split("=", 1)
                env_vars[key] = val

API_KEY = env_vars.get("GEMINI_API_KEY")
if not API_KEY:
    print("❌ GEMINI_API_KEY not found in .env. Exiting.")
    sys.exit(1)

# 2. Run Scraping Tools (Link)
print("🚀 Triggering Scraping Scripts...")
python_exe = sys.executable
subprocess.run([python_exe, "tools/scrape_reddit.py"], check=True)
subprocess.run([python_exe, "tools/scrape_html_events.py"], check=True)

# 3. Read Raw Data
print("📦 Reading Raw JSON Data...")
try:
    with open(".tmp/reddit_raw.json", "r", encoding="utf-8") as f:
        reddit_data = json.load(f)
except Exception:
    reddit_data = []

try:
    with open(".tmp/html_raw.json", "r", encoding="utf-8") as f:
        html_data = json.load(f)
except Exception:
    html_data = []

# Format payload (truncating to a safe token size representing roughly 400KB data)
raw_text_payload = json.dumps({"reddit": reddit_data, "html": html_data})[:400000]

# 4. Push to Large Language Model (Gemini REST API)
print(f"🧠 Sending {len(raw_text_payload)} bytes of context to Gemini...")

prompt = f"""You are the System Pilot extracting event data from raw scrapings of South Lake Tahoe.
Identify any major, high-demand events (e.g. festivals, major concerts, large sporting events). 
Ignore small local postings or general advice.

Data Context:
{raw_text_payload}

REQUIRED OUTPUT FORMAT (Return strictly valid JSON Array of Objects, no markdown formatting blocks at the start/end):
[
  {{
    "event_name": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "verification_url": "string (URL to source or event page)",
    "description": "string (Short 1-2 sentence description)",
    "demand_impact": "string (High | Medium)",
    "location": "string"
  }}
]
"""

gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
payload_str = json.dumps({
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "temperature": 0.1,
        "responseMimeType": "application/json"
    }
})
payload_bytes = payload_str.encode('utf-8')

req = urllib.request.Request(gemini_url, data=payload_bytes, headers={'Content-Type': 'application/json'})

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    response = urllib.request.urlopen(req, context=ctx, timeout=60)
    response_body = response.read().decode('utf-8')
    data = json.loads(response_body)
    
    generated_text = data['candidates'][0]['content']['parts'][0]['text']
    try:
        events_json = json.loads(generated_text)
        print(f"✅ Extracted {len(events_json)} structured events.")
    except json.JSONDecodeError:
        print("❌ Failed to parse LLM output as JSON.")
        events_json = []

except urllib.error.URLError as e:
    print(f"❌ LLM Request Failed: {e}")
    sys.exit(1)

# 5. Push Validated Structured Event Block to tmp
with open(".tmp/payload.json", "w", encoding="utf-8") as f:
    json.dump(events_json, f, indent=2)

print("📝 Structured Event Payload generated at .tmp/payload.json")

# 6. Trigger Payload/Frontend builder
print("🌐 Triggering final Calendar build...")
subprocess.run([python_exe, "tools/build_calendar.py"], check=True)

print("🎉 Navigation Run Complete! The Source of Truth calendar is updated.")
