from datetime import timedelta
from django.utils import timezone
from core.models import NoFapEntry


def get_nofap_streak(user):
    """
    Calculate current NoFap streak.
    Relapse OR missing day resets streak.
    """
    today = timezone.now().date()
    streak = 0
    current_day = today

    while True:
        entry = NoFapEntry.objects.filter(
            user=user,
            date=current_day
        ).first()

        if not entry or not entry.is_clean:
            break

        streak += 1
        current_day -= timedelta(days=1)

    return streak
