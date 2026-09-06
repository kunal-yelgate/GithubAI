from collections import Counter
from datetime import datetime


def analyze_commits(commits: list):

    if not commits:
        return {
            "total_analyzed": 0,
            "contributors": [],
            "commits_by_contributor": {},
            "first_commit": None,
            "latest_commit": None
        }

    contributor_counter = Counter()

    commit_dates = []

    for commit in commits:

        author = commit.get("author")

        if author:
            username = author.get("login")

            if username:
                contributor_counter[username] += 1

        commit_info = commit.get("commit", {})
        author_info = commit_info.get("author")

        if author_info:

            date = author_info.get("date")

            if date:
                commit_dates.append(date)

    commit_dates.sort()

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
        )
    }