from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from django.utils import timezone

from core.services.scores import calculate_daily_score
from core.services.summaries import weekly_summary, monthly_summary


def export_life_pdf(user):
    buffer = BytesIO()  # ✅ CORRECT

    styles = getSampleStyleSheet()
    story = []

    today = timezone.now().date()
    year = today.year

    # -------- Title --------
    story.append(Paragraph("Life Report", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"User: {user.username}", styles["Normal"]))
    story.append(Paragraph(f"Year: {year}", styles["Normal"]))
    story.append(Paragraph(f"Generated on: {today}", styles["Normal"]))
    story.append(Spacer(1, 20))

    # -------- Monthly Summary --------
    monthly = monthly_summary(user, today.year, today.month)

    story.append(Paragraph("Monthly Summary", styles["Heading2"]))
    story.append(Paragraph(f"Average Score: {monthly['avg_score']}%", styles["Normal"]))
    story.append(Paragraph(f"Best Day Score: {monthly['best_day']}%", styles["Normal"]))
    story.append(Paragraph(f"Worst Day Score: {monthly['worst_day']}%", styles["Normal"]))
    story.append(
        Paragraph(
            f"NoFap Clean Days: {monthly['nofap_clean_days']} / {monthly['total_days']}",
            styles["Normal"]
        )
    )
    story.append(Spacer(1, 16))

    # -------- Weekly Summary --------
    story.append(Paragraph("Weekly Summary", styles["Heading2"]))

    for day in weekly_summary(user):
        story.append(
            Paragraph(
                f"{day['date']} — {day['score']}% ({day['status']})",
                styles["Normal"]
            )
        )

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    doc.build(story)

    buffer.seek(0)  # ✅ VERY IMPORTANT
    return buffer
