from collections import Counter
from datetime import datetime


def analyze_activity(commits: list):

    if not commits:
        return {
            "commits_by_month": {},
            "commits_by_weekday": {},
            "commits_by_hour": {}
        }

    monthly = Counter()
    weekdays = Counter()
    hours = Counter()

    for commit in commits:

        author_info = (
            commit
            .get("commit", {})
            .get("author")
        )

        if not author_info:
            continue

        date_string = author_info.get("date")

        if not date_string:
            continue

        try:

            date = datetime.fromisoformat(
                date_string.replace("Z", "+00:00")
            )

        except ValueError:

            continue

        monthly[
            date.strftime("%Y-%m")
        ] += 1

        weekdays[
            date.strftime("%A")
        ] += 1

        hours[
            date.hour
        ] += 1

    return {
        "commits_by_month": dict(
            sorted(monthly.items())
        ),

        "commits_by_weekday": dict(
            weekdays
        ),

        "commits_by_hour": dict(
            sorted(hours.items())
        )
    }