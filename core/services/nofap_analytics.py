from datetime import timedelta
from django.utils import timezone
from core.models import NoFapEntry


def current_nofap_streak(user):
    today = timezone.now().date()
    streak = 0

    day = today
    while True:
        entry = NoFapEntry.objects.filter(user=user, date=day, is_clean=True).first()
        if entry:
            streak += 1
            day -= timedelta(days=1)
        else:
            break

    return streak


def best_nofap_streak(user):
    entries = NoFapEntry.objects.filter(user=user).order_by("date")

    best = 0
    current = 0
    prev_date = None

    for e in entries:
        if e.is_clean:
            if prev_date and (e.date - prev_date).days == 1:
                current += 1
            else:
                current = 1
            best = max(best, current)
        else:
            current = 0

        prev_date = e.date

    return best


def relapse_count_last_30_days(user):
    since = timezone.now().date() - timedelta(days=30)
    return NoFapEntry.objects.filter(
        user=user,
        date__gte=since,
        is_clean=False
    ).count()


def monthly_nofap_stats(user, year, month):
    from calendar import monthrange

    total_days = monthrange(year, month)[1]
    clean = NoFapEntry.objects.filter(
        user=user,
        date__year=year,
        date__month=month,
        is_clean=True
    ).count()

    relapse = total_days - clean
    return clean, relapse
