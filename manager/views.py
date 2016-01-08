import datetime
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def main(request):
    if (not request.user.is_deanery and not request.user.is_admin) or not request.user.is_active:
        raise PermissionDenied
    context = {}
    return render(request, 'manager/main.html', context)

@login_required
def schedule(request):
    if (not request.user.is_deanery and not request.user.is_admin) or not request.user.is_active:
        raise PermissionDenied
    context = {}
    today = timezone.now().date()
    if today >= datetime.date(today.year, 1, 1) and today <= datetime.date(today.year, 5, 31):
        semester = True
        startStudyYear = (today.year - 1) % 100
    else:
        semester = False
        startStudyYear = today.year % 100
    context['start_study_year'] = startStudyYear
    context['semester'] = semester
    return render(request, 'manager/schedule.html', context)

@login_required
def users(request):
    if (not request.user.is_deanery and not request.user.is_admin) or not request.user.is_active:
        raise PermissionDenied
    context = {}
    return render(request, 'manager/users.html', context)
