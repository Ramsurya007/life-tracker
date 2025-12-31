from core.models import Habit, DailyEntry
from core.services.nofap import get_nofap_streak


def calculate_daily_score(user, date):
    habits = Habit.objects.filter(user=user, is_active=True)

    max_score = habits.count()
    earned_score = 0
    bad_habit_failed = False

    for habit in habits:
        entry = DailyEntry.objects.filter(
            habit=habit,
            date=date
        ).first()

        if entry:
            earned_score += entry.status

            if habit.is_bad and entry.status == 0:
                bad_habit_failed = True
                earned_score -= 1  # penalty
        else:
            if habit.is_bad:
                bad_habit_failed = True
                earned_score -= 1

    # NoFap penalty
    nofap_streak = get_nofap_streak(user)
    nofap_relapse = nofap_streak == 0

    if nofap_relapse:
        earned_score -= 2

    if max_score <= 0:
        return {"score": 0, "status": "NO DATA"}

    percentage = max(0, int((earned_score / max_score) * 100))

    if percentage >= 80:
        status = "STRONG"
    elif percentage >= 60:
        status = "AVERAGE"
    else:
        status = "WARNING"

    return {
        "score": percentage,
        "status": status,
        "bad_habit_failed": bad_habit_failed,
        "nofap_relapse": nofap_relapse
    }
