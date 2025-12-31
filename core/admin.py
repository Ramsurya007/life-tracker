from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Habit, DailyEntry, NoFapEntry, DailyNote
@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'is_bad', 'is_active', 'created_at')
    list_filter = ('category', 'is_bad', 'is_active')
    search_fields = ('name',)


@admin.register(DailyEntry)
class DailyEntryAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'status')
    list_filter = ('date',)
    ordering = ('-date',)


@admin.register(NoFapEntry)
class NoFapEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'is_clean')
    list_filter = ('is_clean', 'date')


@admin.register(DailyNote)
class DailyNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood')
    list_filter = ('mood', 'date')
