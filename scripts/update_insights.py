#!/usr/bin/env python3
"""
Update insights.html to include the newly generated article.
"""

import os
import json
import re

def load_latest_article():
    """Load metadata from the latest generated article."""
    try:
        with open('scripts/latest_article.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No latest article found, skipping insights update")
        return None

def create_article_card(metadata):
    """Create HTML for an article card."""
    return f'''
                <!-- Article: {metadata['title'][:30]}... -->
                <article class="insight-card">
                    <div class="insight-meta">
                        <span class="insight-category">{metadata['category']}</span>
                        <span class="insight-date">{metadata['date']}</span>
                    </div>
                    <h2><a href="{metadata['filename']}">{metadata['title']}</a></h2>
                    <p>{metadata['subtitle']}</p>
                    <a href="{metadata['filename']}" class="insight-link">Read More <span>&rarr;</span></a>
                </article>
'''

def update_insights_page(metadata):
    """Add new article to the top of the insights grid."""
    with open('insights.html', 'r') as f:
        content = f.read()

    # Find the insights grid and add new article at the top
    new_card = create_article_card(metadata)

    # Insert after <div class="insights-grid">
    pattern = r'(<div class="insights-grid">)'
    replacement = r'\1' + new_card

    updated_content = re.sub(pattern, replacement, content, count=1)

    with open('insights.html', 'w') as f:
        f.write(updated_content)

    print(f"Added '{metadata['title'][:40]}...' to insights.html")

def main():
    metadata = load_latest_article()
    if metadata:
        update_insights_page(metadata)

        # Clean up
        os.remove('scripts/latest_article.json')
        print("Cleaned up temporary files")

if __name__ == "__main__":
    main()
