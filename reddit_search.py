#!/usr/bin/env python3
"""
reddit_search.py — Reddit search tool for the Ridgewood skill

Usage:
  python reddit_search.py --query "paris underrated neighborhoods locals"
  python reddit_search.py --query "bars locals" --subreddit paris --limit 15
  python reddit_search.py --query "instead of montmartre" --min-score 3

Output: JSON array of posts with title, score, date, url, and top comments.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

try:
    import praw
except ImportError:
    print("Missing dependency: run  pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # .env loading is optional if env vars are set directly


def build_reddit_client():
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    if not client_id or not client_secret:
        print(
            "Error: REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET must be set.\n"
            "Copy .env.example to .env and fill in your credentials.",
            file=sys.stderr,
        )
        sys.exit(1)
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="ridgewood-skill/1.0 (read-only)",
    )


def search(query, subreddit=None, limit=10, min_score=5, max_age_years=2):
    reddit = build_reddit_client()

    cutoff = datetime.now(timezone.utc).timestamp() - (max_age_years * 365.25 * 86400)

    target = reddit.subreddit(subreddit) if subreddit else reddit.subreddit("all")

    results = []
    # Over-fetch to account for score/age filtering
    for post in target.search(query, sort="relevance", time_filter="year", limit=limit * 4):
        if post.score < min_score:
            continue
        if post.created_utc < cutoff:
            continue

        post.comments.replace_more(limit=0)
        top_comments = []
        for comment in sorted(post.comments.list(), key=lambda c: c.score, reverse=True)[:5]:
            if hasattr(comment, "body") and comment.score >= 3 and len(comment.body) > 30:
                top_comments.append({
                    "score": comment.score,
                    "text": comment.body[:600].strip(),
                })

        results.append({
            "title": post.title,
            "score": post.score,
            "num_comments": post.num_comments,
            "date": datetime.fromtimestamp(post.created_utc, tz=timezone.utc).strftime("%Y-%m"),
            "subreddit": post.subreddit.display_name,
            "url": f"https://reddit.com{post.permalink}",
            "selftext_preview": post.selftext[:300].strip() if post.selftext else "",
            "top_comments": top_comments,
        })

        if len(results) >= limit:
            break

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Search Reddit and return structured results for the Ridgewood skill."
    )
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--subreddit", default=None, help="Restrict to a specific subreddit (e.g. 'paris')")
    parser.add_argument("--limit", type=int, default=10, help="Max results to return (default: 10)")
    parser.add_argument("--min-score", type=int, default=5, dest="min_score",
                        help="Minimum post score to include (default: 5)")
    parser.add_argument("--max-age-years", type=float, default=2, dest="max_age_years",
                        help="Maximum post age in years (default: 2)")
    args = parser.parse_args()

    results = search(
        query=args.query,
        subreddit=args.subreddit,
        limit=args.limit,
        min_score=args.min_score,
        max_age_years=args.max_age_years,
    )

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
