#!/usr/bin/env python3
"""
Generate a new article for Privanon using Claude API.
Topics rotate through defense communications and security themes.
"""

import os
import json
import random
from datetime import datetime
from anthropic import Anthropic

# Topics to rotate through
TOPICS = [
    {
        "title": "Quantum Computing Threats to Current Encryption Standards",
        "category": "Threat Analysis",
        "focus": "How quantum computers will break RSA and ECC, timeline estimates, and why organizations need to prepare now for post-quantum cryptography"
    },
    {
        "title": "Supply Chain Attacks: The Hidden Vulnerability in Defense Hardware",
        "category": "Security",
        "focus": "Hardware implants, firmware compromises, and why US-based manufacturing matters for defense communications equipment"
    },
    {
        "title": "Mesh Networking for Tactical Operations: When Infrastructure Fails",
        "category": "Technology",
        "focus": "How mesh networks provide resilience when traditional infrastructure is destroyed or unavailable, practical implementations"
    },
    {
        "title": "The Evolution of SIGINT: Modern Signals Intelligence Threats",
        "category": "Threat Analysis",
        "focus": "How adversary SIGINT capabilities have evolved, what they can intercept, and defensive countermeasures"
    },
    {
        "title": "Secure Communications in Denied Environments",
        "category": "Strategy",
        "focus": "Operating when GPS is jammed, networks are compromised, and adversaries control the spectrum"
    },
    {
        "title": "Hardware Security Modules: The Foundation of Trust",
        "category": "Technology",
        "focus": "Why HSMs matter for tactical communications, how they work, and what to look for in defense-grade implementations"
    },
    {
        "title": "5G Security Implications for Defense Operations",
        "category": "Threat Analysis",
        "focus": "New attack surfaces introduced by 5G, network slicing vulnerabilities, and securing military use of commercial 5G"
    },
    {
        "title": "Offline Authentication: Identity Verification Without Connectivity",
        "category": "Technology",
        "focus": "Cryptographic techniques for verifying identity when disconnected from central servers"
    },
    {
        "title": "Counter-Drone Communications Security",
        "category": "Strategy",
        "focus": "Securing command and control links against jamming and hijacking in the counter-UAS domain"
    },
    {
        "title": "The Insider Threat in Secure Communications",
        "category": "Security",
        "focus": "Technical and procedural controls for protecting against compromised personnel with legitimate access"
    }
]

def get_existing_articles():
    """Get list of existing article files to avoid duplicates."""
    existing = []
    for f in os.listdir('.'):
        if f.startswith('insight-') and f.endswith('.html'):
            existing.append(f)
    return existing

def select_topic(existing_articles):
    """Select a topic that hasn't been covered recently."""
    # Simple rotation - pick randomly from topics
    # In production, could track which topics have been used
    return random.choice(TOPICS)

def generate_slug(title):
    """Generate URL-friendly slug from title."""
    slug = title.lower()
    slug = slug.replace(':', '')
    slug = slug.replace("'", '')
    slug = '-'.join(slug.split())
    return f"insight-{slug[:50]}"

def generate_article(topic):
    """Generate article content using Claude API."""
    client = Anthropic()

    prompt = f"""Write a professional article for Privanon LLC, a defense technology company specializing in secure communications.

TOPIC: {topic['title']}
CATEGORY: {topic['category']}
FOCUS: {topic['focus']}

REQUIREMENTS:
- Write 800-1000 words
- Professional, authoritative tone suitable for defense/intelligence audience
- Include practical insights, not just theory
- Structure with clear H2 headings
- End with how Privanon's solutions (PTUS, IMSI Obfuscation, Dynamic Port Hopping) address these challenges
- Do not use markdown formatting - output plain text with heading markers

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
TITLE: [Article title]
SUBTITLE: [One sentence subtitle]
CONTENT:
[Article content with ##HEADING## markers for H2 headings]

Example heading format: ##The Challenge of Modern Threats##"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text

def parse_article(raw_content):
    """Parse the generated content into components."""
    lines = raw_content.strip().split('\n')

    title = ""
    subtitle = ""
    content_lines = []
    in_content = False

    for line in lines:
        if line.startswith('TITLE:'):
            title = line.replace('TITLE:', '').strip()
        elif line.startswith('SUBTITLE:'):
            subtitle = line.replace('SUBTITLE:', '').strip()
        elif line.startswith('CONTENT:'):
            in_content = True
        elif in_content:
            content_lines.append(line)

    content = '\n'.join(content_lines)
    return title, subtitle, content

def format_content_html(content):
    """Convert content with ##HEADING## markers to HTML."""
    import re

    # Convert ##Heading## to <h2>Heading</h2>
    content = re.sub(r'##([^#]+)##', r'<h2>\1</h2>', content)

    # Wrap paragraphs
    paragraphs = content.split('\n\n')
    formatted = []
    for p in paragraphs:
        p = p.strip()
        if p.startswith('<h2>'):
            formatted.append(p)
        elif p:
            formatted.append(f'<p>{p}</p>')

    return '\n\n                '.join(formatted)

def create_article_html(title, subtitle, content, category, slug):
    """Create the full HTML page for the article."""
    date = datetime.now().strftime('%B %Y')

    html_content = format_content_html(content)

    template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{subtitle}">
    <title>{title} | Privanon LLC</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="index.html" class="logo">
                <svg class="brand-mark" viewBox="0 0 100 100" fill="none" width="24" height="24" style="margin-right: 8px;"><path d="M20 20 H50 V90 C30 90 20 70 20 40 V20 Z" fill="currentColor"/><rect x="55" y="20" width="25" height="15" fill="#00d4ff"/><rect x="55" y="40" width="20" height="15" fill="currentColor"/><rect x="55" y="60" width="15" height="15" fill="currentColor"/><rect x="55" y="80" width="10" height="10" fill="currentColor"/></svg>
                PRIVANON
                <span class="logo-division">A Division of BKW</span>
            </a>
            <ul class="nav-links">
                <li><a href="index.html#solutions">Capabilities</a></li>
                <li><a href="index.html#technology">Technology</a></li>
                <li><a href="insights.html" class="active">Insights</a></li>
                <li><a href="index.html#contact" class="nav-cta">Contact</a></li>
            </ul>
...
                <div class="footer-links">
                    <h4>Capabilities</h4>
                    <ul>
                        <li><a href="index.html#solutions">PTUS</a></li>
                        <li><a href="index.html#solutions">IMSI Obfuscation</a></li>
                        <li><a href="index.html#solutions">Port Hopping</a></li>
                    </ul>
                </div>
...
            <div class="footer-bottom">
                <p>&copy; 2026 Privanon LLC. A Division of BKW. All rights reserved.</p>
                <p class="footer-legal">ITAR and export control regulations may apply to our products and services.</p>
            </div>
            <button class="mobile-menu-btn" aria-label="Menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </nav>

    <!-- Article -->
    <article class="article-page">
        <div class="container">
            <div class="article-header">
                <a href="insights.html" class="back-link">&larr; Back to Insights</a>
                <div class="insight-meta">
                    <span class="insight-category">{category}</span>
                    <span class="insight-date">{date}</span>
                </div>
                <h1>{title}</h1>
                <p class="article-subtitle">{subtitle}</p>
            </div>

            <div class="article-content">
                {html_content}

                <div class="article-cta">
                    <h3>Secure Your Communications</h3>
                    <p>Contact Privanon for a briefing on how our technologies can address your operational security requirements.</p>
                    <a href="index.html#contact" class="btn btn-primary">Request Briefing</a>
                </div>
            </div>
        </div>
    </article>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="index.html" class="logo">
                        <svg class="brand-mark" viewBox="0 0 100 100" fill="none" width="24" height="24" style="margin-right: 8px;"><path d="M20 20 H50 V90 C30 90 20 70 20 40 V20 Z" fill="currentColor"/><rect x="55" y="20" width="25" height="15" fill="#00d4ff"/><rect x="55" y="40" width="20" height="15" fill="currentColor"/><rect x="55" y="60" width="15" height="15" fill="currentColor"/><rect x="55" y="80" width="10" height="10" fill="currentColor"/></svg>
                        PRIVANON
                    </a>
                    <p>Defense-grade communications and network security.</p>
                </div>
                <div class="footer-links">
                    <h4>Solutions</h4>
                    <ul>
                        <li><a href="index.html#solutions">PTUS</a></li>
                        <li><a href="index.html#solutions">IMSI Obfuscation</a></li>
                        <li><a href="index.html#solutions">Port Hopping</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="index.html#about">About</a></li>
                        <li><a href="index.html#technology">Technology</a></li>
                        <li><a href="insights.html">Insights</a></li>
                        <li><a href="gear.html">Gear</a></li>
                        <li><a href="index.html#contact">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Privanon LLC. A Division of BKW. All rights reserved.</p>
                <p class="footer-legal">ITAR and export control regulations may apply to our products and services.</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>'''

    return template

def main():
    existing = get_existing_articles()
    print(f"Found {len(existing)} existing articles")

    topic = select_topic(existing)
    print(f"Selected topic: {topic['title']}")

    print("Generating article with Claude...")
    raw_content = generate_article(topic)

    title, subtitle, content = parse_article(raw_content)
    slug = generate_slug(title)

    print(f"Title: {title}")
    print(f"Slug: {slug}")

    html = create_article_html(title, subtitle, content, topic['category'], slug)

    filename = f"{slug}.html"
    with open(filename, 'w') as f:
        f.write(html)

    print(f"Created: {filename}")

    # Save metadata for insights page update
    metadata = {
        "filename": filename,
        "title": title,
        "subtitle": subtitle,
        "category": topic['category'],
        "date": datetime.now().strftime('%B %Y')
    }

    with open('scripts/latest_article.json', 'w') as f:
        json.dump(metadata, f)

    print("Done!")

if __name__ == "__main__":
    main()
