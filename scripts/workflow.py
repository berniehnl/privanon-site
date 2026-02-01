#!/usr/bin/env python3
"""
Privanon Content Workflow: Generate article, update site, and post to X.
Rate limited to 3 posts per day.
"""

import os
import sys
import json
import argparse
from datetime import datetime, date

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from generate_article import main as generate_article
from update_insights import main as update_insights
from post_to_x import post_article, post_custom

# Rate limit tracking file
RATE_LIMIT_FILE = os.path.join(os.path.dirname(__file__), '.post_history.json')
MAX_POSTS_PER_DAY = 3


def load_post_history():
    """Load posting history."""
    try:
        with open(RATE_LIMIT_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"posts": []}


def save_post_history(history):
    """Save posting history."""
    with open(RATE_LIMIT_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def get_today_post_count():
    """Get number of posts made today."""
    history = load_post_history()
    today = date.today().isoformat()
    return sum(1 for p in history["posts"] if p.get("date") == today)


def record_post(post_type, content_preview):
    """Record a post in history."""
    history = load_post_history()
    history["posts"].append({
        "date": date.today().isoformat(),
        "time": datetime.now().isoformat(),
        "type": post_type,
        "preview": content_preview[:50]
    })
    # Keep only last 30 days of history
    cutoff = date.today().isoformat()[:7]  # Keep current month
    history["posts"] = [p for p in history["posts"] if p["date"][:7] >= cutoff]
    save_post_history(history)


def can_post():
    """Check if we can post (rate limit)."""
    count = get_today_post_count()
    remaining = MAX_POSTS_PER_DAY - count
    return remaining > 0, remaining


def run_full_workflow(dry_run=False, skip_post=False):
    """Run the complete content workflow."""
    print("=" * 50)
    print("PRIVANON CONTENT WORKFLOW")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # Check rate limit
    can, remaining = can_post()
    print(f"\n[*] Daily post limit: {remaining}/{MAX_POSTS_PER_DAY} remaining")

    if not can and not skip_post and not dry_run:
        print("[!] Daily post limit reached. Use --skip-post to generate without posting.")
        return False

    # Step 1: Generate Article
    print("\n--- STEP 1: Generate Article ---")
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    generate_article()

    # Load metadata before update_insights deletes it
    metadata = None
    try:
        with open('scripts/latest_article.json', 'r') as f:
            metadata = json.load(f)
    except FileNotFoundError:
        print("[!] No article metadata found")

    # Step 2: Update Insights Page
    print("\n--- STEP 2: Update Insights Page ---")
    update_insights()

    # Step 3: Post to X
    if skip_post:
        print("\n--- STEP 3: Post to X [SKIPPED] ---")
    elif metadata is None:
        print("\n--- STEP 3: Post to X [SKIPPED - no metadata] ---")
    else:
        print("\n--- STEP 3: Post to X ---")
        success = post_article(metadata=metadata, dry_run=dry_run)
        if success and not dry_run:
            record_post("article", metadata.get("title", "Unknown"))

    print("\n" + "=" * 50)
    print("WORKFLOW COMPLETE")
    print("=" * 50)

    # Reminder about deployment
    print("\nNext steps:")
    print("1. Review the generated article")
    print("2. Deploy to Hostinger:")
    print("   tar -czvf deploy.tar.gz -C . .")
    print("   # Then use MCP: hosting_deployStaticWebsite")

    return True


def show_status():
    """Show current posting status."""
    can, remaining = can_post()
    history = load_post_history()
    today = date.today().isoformat()
    today_posts = [p for p in history["posts"] if p.get("date") == today]

    print("PRIVANON POSTING STATUS")
    print("-" * 30)
    print(f"Date: {today}")
    print(f"Posts today: {len(today_posts)}/{MAX_POSTS_PER_DAY}")
    print(f"Remaining: {remaining}")
    print()

    if today_posts:
        print("Today's posts:")
        for p in today_posts:
            print(f"  - {p['time'][11:16]} | {p['type']}: {p['preview']}...")


def main():
    parser = argparse.ArgumentParser(
        description='Privanon Content Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python workflow.py                    # Full workflow (generate + update + post)
  python workflow.py --dry-run          # Preview without posting
  python workflow.py --skip-post        # Generate article without posting
  python workflow.py --status           # Check daily post count
  python workflow.py --post-custom "msg" # Post custom message
        """
    )

    parser.add_argument('--dry-run', action='store_true',
                        help='Run workflow but do not actually post')
    parser.add_argument('--skip-post', action='store_true',
                        help='Generate article but skip posting to X')
    parser.add_argument('--status', action='store_true',
                        help='Show posting status for today')
    parser.add_argument('--post-custom', type=str, metavar='MSG',
                        help='Post a custom message (respects rate limit)')

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.post_custom:
        can, remaining = can_post()
        if not can:
            print(f"[!] Daily limit reached ({MAX_POSTS_PER_DAY} posts). Try again tomorrow.")
            return
        success = post_custom(args.post_custom, dry_run=args.dry_run)
        if success and not args.dry_run:
            record_post("custom", args.post_custom)
    else:
        run_full_workflow(dry_run=args.dry_run, skip_post=args.skip_post)


if __name__ == "__main__":
    main()
