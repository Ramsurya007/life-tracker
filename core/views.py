from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from core.services.scores import calculate_daily_score
from core.services.nofap import get_nofap_streak
from django.shortcuts import redirect
from django.contrib import messages
from core.services.summaries import weekly_summary
from core.models import Habit, DailyEntry, NoFapEntry, DailyNote
from core.services.summaries import monthly_summary
from core.services.summaries import yearly_heatmap
from core.services.summaries import weekly_summary, monthly_summary
from calendar import monthrange
from django.utils import timezone
from django.http import HttpResponse
from core.services.export import export_life_excel
from core.services.pdf_export import export_life_pdf
from core.services.nofap_analytics import (
    current_nofap_streak,
    best_nofap_streak,
    relapse_count_last_30_days,
    monthly_nofap_stats
)





@login_required
def dashboard(request):
    today = timezone.now().date()

    score_data = calculate_daily_score(request.user, today)
    nofap_streak = get_nofap_streak(request.user)
    monthly = monthly_summary(
    request.user,
    today.year,
    today.month
)
    weekly = weekly_summary(request.user)
    heatmap = yearly_heatmap(request.user, today.year)

    context = {
    "score": score_data,
    "nofap_streak": nofap_streak,
    "today": today,
    "weekly": weekly,
    "monthly": monthly,
    "heatmap": heatmap,
}
    # Weekly chart data
    weekly_labels = [str(d["date"]) for d in weekly]
    weekly_scores = [d["score"] for d in weekly]

    # Monthly chart data (daily scores of this month)


    days_in_month = monthrange(today.year, today.month)[1]
    monthly_labels = list(range(1, days_in_month + 1))
    monthly_scores = [
        calculate_daily_score(request.user, timezone.datetime(today.year, today.month, day).date())["score"]
        for day in monthly_labels
    ]

    context.update({
        "weekly_labels": weekly_labels,
        "weekly_scores": weekly_scores,
        "monthly_labels": monthly_labels,
        "monthly_scores": monthly_scores,
    })
    current_streak = current_nofap_streak(request.user)
    best_streak = best_nofap_streak(request.user)
    relapses_30 = relapse_count_last_30_days(request.user)

    nofap_clean, nofap_relapse = monthly_nofap_stats(
        request.user, today.year, today.month
    )

    context.update({
        "current_streak": current_streak,
        "best_streak": best_streak,
        "relapses_30": relapses_30,
        "nofap_clean": nofap_clean,
        "nofap_relapse": nofap_relapse,
    })


    return render(request, "dashboard.html", context)

@login_required
def daily_track(request):
    today = timezone.now().date()
    habits = Habit.objects.filter(user=request.user, is_active=True)

    if request.method == "POST":
        # 1️⃣ Save habits
        for habit in habits:
            status = request.POST.get(f"habit_{habit.id}")

            if status is not None:
                DailyEntry.objects.update_or_create(
                    habit=habit,
                    date=today,
                    defaults={"status": float(status)}
                )

        # 2️⃣ Save NoFap
        nofap_status = request.POST.get("nofap")

        if not nofap_status:
            messages.error(request, "NoFap status is mandatory.")
            return redirect("daily-track")

        is_clean = nofap_status == "clean"
        relapse_reason = request.POST.get("relapse_reason", "")

        NoFapEntry.objects.update_or_create(
            user=request.user,
            date=today,
            defaults={
                "is_clean": is_clean,
                "relapse_reason": relapse_reason if not is_clean else ""
            }
        )

        # 3️⃣ Save Daily Note
        note = request.POST.get("note", "").strip()
        mood = request.POST.get("mood")

        if not note:
            messages.error(request, "Daily note is mandatory.")
            return redirect("daily-track")

        DailyNote.objects.update_or_create(
            user=request.user,
            date=today,
            defaults={
                "note": note,
                "mood": mood
            }
        )

        messages.success(request, "Day recorded successfully.")
        return redirect("dashboard")

    context = {
        "habits": habits,
        "today": today
    }

    return render(request, "daily_track.html", context)

@login_required
def day_detail(request, date):
    from datetime import datetime

    day = datetime.strptime(date, "%Y-%m-%d").date()

    score = calculate_daily_score(request.user, day)

    habits = Habit.objects.filter(user=request.user, is_active=True)
    entries = {
        e.habit_id: e
        for e in DailyEntry.objects.filter(habit__in=habits, date=day)
    }

    nofap = NoFapEntry.objects.filter(user=request.user, date=day).first()
    note = DailyNote.objects.filter(user=request.user, date=day).first()

    context = {
        "day": day,
        "score": score,
        "habits": habits,
        "entries": entries,
        "nofap": nofap,
        "note": note,
    }
    return render(request, "day_detail.html", context)

@login_required
def export_excel(request):
    wb = export_life_excel(request.user)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="life_report.xlsx"'

    wb.save(response)
    return response


@login_required
def export_pdf(request):
    buffer = export_life_pdf(request.user)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="life_report.pdf"'

    return response

@login_required
def onboarding(request):
    if Habit.objects.filter(user=request.user).exists():
        return redirect('dashboard')

    if request.method == 'POST':
        habits = request.POST.getlist('habits')

        for h in habits:
            Habit.objects.create(
                user=request.user,
                name=h,
                category="General",
                is_bad=False,
                is_active=True
            )

        return redirect('dashboard')

    return render(request, 'onboarding.html')
