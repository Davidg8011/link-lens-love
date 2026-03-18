import json
import os
import re

def strip_emojis(text):
    if not text:
        return ""
    # Remove emoji characters by dropping non-ascii
    return text.encode('ascii', 'ignore').decode('ascii').strip()

def generate_html(events):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>South Lake Tahoe Calendar</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body { 
            font-family: 'Outfit', sans-serif; 
            background: #020617; 
            color: #f8fafc; 
            margin: 0; 
            padding: 3rem 2rem; 
        }
        h1 { 
            text-align: center; 
            font-weight: 1000; 
            font-size: 3.8rem;
            background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 50%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            letter-spacing: -1px;
        }
        p.subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 1.25rem;
            margin-bottom: 4rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .event-grid { 
            column-count: 3; 
            column-gap: 2.5rem; 
        }
        @media (max-width: 1100px) { .event-grid { column-count: 2; } }
        @media (max-width: 768px) { .event-grid { column-count: 1; } }
        
        .card { 
            break-inside: avoid;
            margin-bottom: 2.5rem;
            background: linear-gradient(160deg, #1e293b, #0f172a); 
            border-radius: 20px; 
            padding: 2.5rem; 
            border-top: 6px solid #38bdf8; 
            box-shadow: 0 20px 40px -15px rgba(56, 189, 248, 0.15);
            border-left: 1px solid rgba(255,255,255,0.03);
            border-right: 1px solid rgba(255,255,255,0.03);
            border-bottom: 1px solid rgba(255,255,255,0.03);
            position: relative; 
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 30px 50px -15px rgba(56, 189, 248, 0.3);
            border-top: 6px solid #60a5fa;
        }
        .date { 
            font-size: 0.95rem; 
            color: #38bdf8; 
            font-weight: 800; 
            text-transform: uppercase; 
            letter-spacing: 0.15em; 
            margin-bottom: 1rem; 
        }
        .title { 
            font-size: 1.6rem; 
            font-weight: 800; 
            margin: 0 0 1.2rem 0; 
            color: #ffffff; 
            line-height: 1.3;
        }
        .desc { 
            font-size: 1.1rem; 
            line-height: 1.6; 
            color: #cbd5e1; 
            margin-bottom: 2rem; 
        }
        .link { 
            display: inline-block; 
            padding: 0.8rem 1.8rem; 
            background: linear-gradient(135deg, #0ea5e9, #2563eb); 
            color: #ffffff; 
            border-radius: 10px; 
            text-decoration: none; 
            font-weight: 700; 
            font-size: 0.95rem; 
            box-shadow: 0 4px 15px -3px rgba(37, 99, 235, 0.4);
            transition: all 0.2s; 
        }
        .link:hover { 
            box-shadow: 0 8px 25px -5px rgba(37, 99, 235, 0.6);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>South Lake Tahoe Calendar</h1>
        <p class="subtitle">Predictive Intelligence for Hotel Demand Surges</p>
        <div class="event-grid">
"""
    events.sort(key=lambda x: x.get('start_date', '9999-12-31'))
    
    for e in events:
        desc = strip_emojis(e.get('description', ''))
        title = strip_emojis(e.get('event_name', ''))
        
        html += f"""
            <div class="card">
                <div class="date">{e.get('start_date')} &ndash; {e.get('end_date')}</div>
                <h2 class="title">{title}</h2>
                <div class="desc">{desc}</div>
                <a href="{e.get('verification_url')}" class="link" target="_blank">Verify Source &nearr;</a>
            </div>"""
        
    html += """
        </div>
    </div>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    input_file = os.path.join(".tmp", "payload.json")
    output_file = "index.html"
    
    if os.path.exists(input_file):
        with open(input_file, "r", encoding="utf-8") as f:
            events = json.load(f)
        
        html_content = generate_html(events)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Generated {output_file} successfully (Updated Styling).")
    else:
        print(f"❌ Input payload not found at {input_file} (Navigation Layer must write this first)")
