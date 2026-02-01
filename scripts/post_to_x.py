#!/usr/bin/env python3
"""
Post article announcements to X (Twitter) for Privanon.
Can be used standalone or called from the workflow script.
"""

import os
import sys
import json
import tweepy
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment from parent directory's .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# X (Twitter) API Credentials
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# Your website URL
SITE_URL = "https://www.privanon.com"


def generate_tweet(title, subtitle, category):
    """Use Claude to generate a compelling tweet for the article."""
    client = Anthropic()

    prompt = f"""Generate a single tweet to promote this defense technology article.

ARTICLE:
Title: {title}
Subtitle: {subtitle}
Category: {category}

REQUIREMENTS:
- Max 250 characters (leave room for the link)
- Professional but engaging tone
- Include 1-2 relevant hashtags like #DefenseTech #CyberSecurity #SIGINT #InfoSec
- Do NOT include the URL (it will be added automatically)
- Make it compelling for defense/intel professionals

Respond with ONLY the tweet text, nothing else."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text.strip()


def post_to_x(text, article_url=None):
    """Post a tweet to X (Twitter)."""
    if not all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]):
        print("[!] X API credentials not configured in .env")
        print("    Required: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET")
        return False

    try:
        client = tweepy.Client(
            consumer_key=X_API_KEY,
            consumer_secret=X_API_SECRET,
            access_token=X_ACCESS_TOKEN,
            access_token_secret=X_ACCESS_TOKEN_SECRET
        )

        # Add URL if provided
        full_text = f"{text}\n\n{article_url}" if article_url else text

        response = client.create_tweet(text=full_text)
        tweet_id = response.data['id']
        print(f"[+] Posted to X! Tweet ID: {tweet_id}")
        print(f"    https://x.com/i/web/status/{tweet_id}")
        return True

    except tweepy.TweepyException as e:
        print(f"[!] Error posting to X: {e}")
        return False


def post_article(metadata=None, dry_run=False):
    """Post an article announcement to X."""
    # Load metadata if not provided
    if metadata is None:
        try:
            with open('scripts/latest_article.json', 'r') as f:
                metadata = json.load(f)
        except FileNotFoundError:
            print("[!] No article metadata found at scripts/latest_article.json")
            print("    Run generate_article.py first")
            return False

    print(f"[*] Generating tweet for: {metadata['title'][:50]}...")
    tweet_text = generate_tweet(
        metadata['title'],
        metadata['subtitle'],
        metadata['category']
    )

    # Build article URL
    article_url = f"{SITE_URL}/{metadata['filename']}"

    print("\n--- GENERATED TWEET ---")
    print(tweet_text)
    print(f"\nLink: {article_url}")
    print("-----------------------")

    if dry_run:
        print("\n[DRY RUN] Tweet not posted. Remove --dry-run to post.")
        return True

    return post_to_x(tweet_text, article_url)


def post_custom(message, dry_run=False):
    """Post a custom message to X."""
    print("\n--- POSTING ---")
    print(message)
    print("---------------")

    if dry_run:
        print("\n[DRY RUN] Tweet not posted.")
        return True

    return post_to_x(message)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Post to X (Twitter) for Privanon')
    parser.add_argument('--article', action='store_true',
                        help='Post announcement for latest article')
    parser.add_argument('--custom', type=str,
                        help='Post a custom message')
    parser.add_argument('--dry-run', action='store_true',
                        help='Generate tweet but do not post')

    args = parser.parse_args()

    if args.custom:
        post_custom(args.custom, dry_run=args.dry_run)
    elif args.article:
        post_article(dry_run=args.dry_run)
    else:
        print("Privanon X Posting Tool")
        print()
        print("Usage:")
        print("  python post_to_x.py --article           # Post latest article")
        print("  python post_to_x.py --article --dry-run # Preview without posting")
        print("  python post_to_x.py --custom 'message'  # Post custom message")


if __name__ == "__main__":
    main()
