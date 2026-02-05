#!/usr/bin/env python3
"""
Privanon Mission Control: Daily Intel Briefing & Social Broadcast.
Integrates with Claude API for summarization and X (Twitter) API for broadcasting.
"""

import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import tweepy
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
# RSS Feeds (Defense & Tech)
FEEDS = {
    "CISA": "https://www.cisa.gov/cybersecurity-advisories.xml",
    "BreakingDefense": "https://breakingdefense.com/feed/",
    "TheHackerNews": "https://feeds.feedburner.com/TheHackersNews"
}

# X (Twitter) API Credentials - REPLACE WITH YOUR KEYS
# Get these from https://developer.x.com
X_API_KEY = os.getenv("X_API_KEY", "YOUR_API_KEY_HERE")
X_API_SECRET = os.getenv("X_API_SECRET", "YOUR_API_SECRET_HERE")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_HERE")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET", "YOUR_ACCESS_TOKEN_SECRET_HERE")

# --- FUNCTIONS ---

def fetch_rss_headlines(feed_url):
    """Fetch top 3 headlines from an RSS feed using standard urllib."""
    try:
        req = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            headlines = []
            # Handle both RSS 2.0 and Atom
            items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')
            for item in items[:3]:
                title = item.find('title') or item.find('{http://www.w3.org/2005/Atom}title')
                link = item.find('link') or item.find('{http://www.w3.org/2005/Atom}link')
                if title is not None:
                    headlines.append({
                        "title": title.text,
                        "link": link.text if link is not None else ""
                    })
            return headlines
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
        return []

def generate_intel_briefing(raw_intel):
    """Use Claude to generate a professional SITREP (Situation Report)."""
    try:
        client = Anthropic() # Uses ANTHROPIC_API_KEY env var
        
        intel_summary = json.dumps(raw_intel, indent=2)
        
        prompt = f"""You are the Privanon Intelligence Officer. 
Analyze the following headlines and generate a concise 'Daily SitRep' (Situation Report).

DATA:
{intel_summary}

REQUIREMENTS:
1. Tone: Professional, Unapologetic, Defense-focused (Hegseth style).
2. Content: 3 main bullet points identifying key threats or shifts in the defense landscape.
3. Call to Action: How Privanon's capabilities (Obfuscation, Rolling Rendezvous) mitigate these shifts.
4. Social: Draft one punchy X (Twitter) post (max 280 chars) to broadcast this intel.

OUTPUT FORMAT (JSON):
{{
  "sitrep_html": "HTML formatted string for the website (just the body content)",
  "tweet_text": "The tweet content"
}}
"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(message.content[0].text)
    except Exception as e:
        print(f"Error generating intel: {e}")
        return None

def post_to_x(text):
    """Post the generated text to X (Twitter)."""
    if "YOUR_API_KEY" in X_API_KEY:
        print("\n[!] X API Keys not configured. Skipping auto-post.")
        return False

    try:
        # Authenticate to X
        client = tweepy.Client(
            consumer_key=X_API_KEY,
            consumer_secret=X_API_SECRET,
            access_token=X_ACCESS_TOKEN,
            access_token_secret=X_ACCESS_TOKEN_SECRET
        )
        
        response = client.create_tweet(text=text)
        print(f"\n[+] Successfully posted to X! Tweet ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"\n[!] Error posting to X: {e}")
        return False

def update_site(sitrep_html):
    """Save the SitRep to a daily file."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"intel-{date_str}.html"
    
    # Simple HTML wrapper
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily SitRep | {date_str}</title>
    <link rel="stylesheet" href="../styles.css">
    <style>body {{ padding: 40px; background: #050505; color: #fff; max-width: 800px; margin: 0 auto; }}</style>
</head>
<body>
    <h1 style="color: #00d4ff;">DAILY SITREP // {date_str}</h1>
    {sitrep_html}
    <br><br>
    <a href="../index.html" style="color: #666; text-decoration: none;">&larr; Return to Base</a>
</body>
</html>"""

    # Create intel directory if not exists
    os.makedirs("privanon-site/intel", exist_ok=True)

    with open(f"privanon-site/intel/{filename}", 'w') as f:
        f.write(full_html)
    
    print(f"Created briefing: privanon-site/intel/{filename}")
    return filename

def main():
    print("--- PRIVANON MISSION CONTROL ---")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # 1. Gather Intel
    all_headlines = {}
    for name, url in FEEDS.items():
        print(f"Gathering intel from {name}...")
        all_headlines[name] = fetch_rss_headlines(url)
    
    # 2. Analyze
    print("Processing with Intelligence AI...")
    intel_data = generate_intel_briefing(all_headlines)
    
    if not intel_data:
        print("Failed to generate intel.")
        return

    # 3. Draft & Save
    with open("scripts/broadcast_draft.txt", "w") as f:
        f.write(intel_data['tweet_text'])
    
    print("\n--- AI DRAFTED BROADCAST (X) ---")
    print(intel_data['tweet_text'])
    print("--------------------------------")
    
    # 4. Auto-Post (If keys present)
    post_to_x(intel_data['tweet_text'])
    
    # 5. Update Site
    update_site(intel_data['sitrep_html'])
    
    print("\nMission Control Complete.")

if __name__ == "__main__":
    main()