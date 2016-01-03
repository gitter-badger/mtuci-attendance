import datetime
from django.utils import timezone
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from attendance.models import StudyWeek

def error403(request):
    response = render_to_response('403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response

def error400(request):
    response = render_to_response('400.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 400
    return response

def error404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def error500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

@login_required
def steward(request):
    if not request.user.is_steward or not request.user.is_active:
        raise PermissionDenied
    context = {}
    steward = request.user
    group = steward.universityGroup
    today = timezone.now().date()
    if not group:
        context['no_group'] = True
    if today > datetime.date(today.year, 5, 31) and \
       today < datetime.date(today.year, 9, 1):
       context['not_study_time'] = True
    if today <= datetime.date(today.year, 12, 31):
        # Первый семестр
        semester = False
    else:
        semester = True
    if not semester:
        # Если 1 семестр
        startStudyYear = today.year % 100
        # Номер текущей учебной недели
        nowWeek = today.isocalendar()[1] - datetime.date(today.year, 9, 1).isocalendar()[1] + 1
    else:
        startStudyYear = (today.year - 1) % 100
        nowWeek = today.isocalendar()[1] - datetime.date(today.year, 2, 8).isocalendar()[1] + 1
    # Получаем номера всех недель из данного семестра
    weeks = [sw['number'] for sw in StudyWeek.objects.filter(startStudyYear=startStudyYear, semester=semester).values('number')]
    # Находим ближайшую неделю к текущей
    activeWeek = 0
    for week in weeks:
        if week <= nowWeek and week > activeWeek:
            activeWeek = week
    # Если существуют, передаём в контекст
    if weeks and activeWeek:
        context['weeks'] = weeks
        context['active_week'] = activeWeek
        context['start_study_year'] = startStudyYear
        context['next_study_year'] = startStudyYear + 1
        context['semester'] = int(semester) + 1
    return render(request, 'app/steward.html', context)
