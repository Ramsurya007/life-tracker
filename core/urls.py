from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('track/', daily_track, name='daily-track'),
    path('day/<str:date>/', day_detail, name='day-detail'),  # 👈 NEW
    path('export/excel/', export_excel, name='export-excel'),
    path('export/pdf/', export_pdf, name='export-pdf'),
    path('onboarding/', onboarding, name='onboarding'),


]
