from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits"
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    is_bad = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class DailyEntry(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="entries"
    )
    date = models.DateField()
    status = models.FloatField(
        choices=[
            (1, 'Done'),
            (0.5, 'Partial'),
            (0, 'Missed')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('habit', 'date')
    def __str__(self):
        return f"{self.habit.name} - {self.date}"


class NoFapEntry(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="nofap_entries"
    )
    date = models.DateField()
    is_clean = models.BooleanField()
    relapse_reason = models.TextField(
        blank=True,
        null=True
    )
    class Meta:
        unique_together = ('user', 'date')
    def __str__(self):
        return f"NoFap - {self.user.username} - {self.date}"

class DailyNote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="daily_notes"
    )
    date = models.DateField(unique=True)
    note = models.TextField()
    mood = models.IntegerField(
        choices=[
            (1, 'Very Bad'),
            (2, 'Bad'),
            (3, 'Neutral'),
            (4, 'Good'),
            (5, 'Excellent')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Note - {self.user.username} - {self.date}"
