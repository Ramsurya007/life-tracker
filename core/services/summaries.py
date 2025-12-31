from datetime import timedelta
from django.utils import timezone
from core.services.scores import calculate_daily_score
from calendar import monthrange
from core.models import NoFapEntry
from datetime import date, timedelta
from django.utils import timezone
from core.services.scores import calculate_daily_score


def weekly_summary(user):
    """
    Returns last 7 days summary.
    """
    today = timezone.now().date()
    week_data = []

    for i in range(7):
        day = today - timedelta(days=i)
        score = calculate_daily_score(user, day)

        week_data.append({
            "date": day,
            "score": score["score"],
            "status": score["status"]
        })

    return reversed(week_data)



def monthly_summary(user, year, month):
    """
    Returns monthly analytics.
    """
    total_days = monthrange(year, month)[1]
    scores = []
    clean_days = 0

    for day in range(1, total_days + 1):
        date = timezone.datetime(year, month, day).date()
        score = calculate_daily_score(user, date)
        scores.append(score["score"])

        nofap = NoFapEntry.objects.filter(
            user=user,
            date=date,
            is_clean=True
        ).exists()

        if nofap:
            clean_days += 1

    avg_score = int(sum(scores) / total_days)
    best_day = max(scores)
    worst_day = min(scores)

    return {
        "avg_score": avg_score,
        "best_day": best_day,
        "worst_day": worst_day,
        "nofap_clean_days": clean_days,
        "total_days": total_days
    }

def yearly_heatmap(user, year):
    """
    Returns list of days with score + color class for a full year.
    """
    start = date(year, 1, 1)
    end = date(year, 12, 31)

    days = []
    current = start

    while current <= end:
        score_data = calculate_daily_score(user, current)
        score = score_data["score"]

        if score >= 80:
            level = "heat-4"
        elif score >= 60:
            level = "heat-3"
        elif score >= 40:
            level = "heat-2"
        else:
            level = "heat-1"

        days.append({
            "date": current,
            "score": score,
            "level": level
        })

        current += timedelta(days=1)

    return days