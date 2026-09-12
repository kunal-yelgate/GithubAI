from collections import Counter
from datetime import datetime


def analyze_commits(commits: list):

    if not commits:
        return {
            "total_analyzed": 0,
            "contributors": [],
            "commits_by_contributor": {},
            "first_commit": None,
            "latest_commit": None,
            "history": []
        }

    contributor_counter = Counter()
    commit_dates = []
    history = []

    for commit in commits:
        author = commit.get("author") or {}
        username = author.get("login") or commit.get("commit", {}).get("author", {}).get("name")

        if username:
            contributor_counter[username] += 1

        commit_info = commit.get("commit", {})
        author_info = commit_info.get("author") or {}
        committer_info = commit_info.get("committer") or {}
        date = author_info.get("date") or committer_info.get("date")
        if date:
            commit_dates.append(date)

        history.append({
            "sha": commit.get("sha"),
            "message": (commit_info.get("message") or "").strip().split("\n")[0],
            "author": username or commit_info.get("author", {}).get("name") or "Unknown",
            "date": date,
            "url": commit.get("html_url") or commit.get("url"),
            "committer": (committer_info.get("name") or "Unknown")
        })

    commit_dates.sort()
    history.sort(key=lambda item: item["date"] or "", reverse=True)

    return {
        "total_analyzed": len(commits),

        "contributors": [
            {
                "username": username,
                "commits": count
            }
            for username, count
            in contributor_counter.most_common()
        ],

        "commits_by_contributor": dict(
            contributor_counter
        ),

        "first_commit": (
            commit_dates[0]
            if commit_dates
            else None
        ),

        "latest_commit": (
            commit_dates[-1]
            if commit_dates
            else None
        ),

        "history": history
    }