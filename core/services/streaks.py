from datetime import timedelta
from django.utils import timezone
from core.models import DailyEntry


def calculate_habit_streak(habit):
    """
    Calculate current streak for a habit.
    Missed day OR missing entry breaks streak.
    """
    today = timezone.now().date()
    streak = 0
    current_day = today

    while True:
        entry = DailyEntry.objects.filter(
            habit=habit,
            date=current_day
        ).first()

        if not entry or entry.status == 0:
            break

        streak += 1
        current_day -= timedelta(days=1)

    return streak
