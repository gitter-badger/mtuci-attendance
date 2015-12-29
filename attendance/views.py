from django.shortcuts import render
from attendance.models import StudyWeek
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied

def generateWeeksNumbersBySEweeks(startWeekNumber, endWeekNumber, weekStep=1):
    '''
    Принимает начальную неделю, конечную неделю и шаг.
    Возвращает список с номерами необходимых недель
    '''
    if not isinstance(startWeekNumber, int) or \
       not isinstance(endWeekNumber, int) or \
       not isinstance(weekStep, int) or \
       startWeekNumber < 1 or startWeekNumber > 25 or \
       endWeekNumber < 1 or endWeekNumber > 25 or \
       weekStep < 0:
       # Если входные данные некорректны, возвращаем None
       return None
    weeksNumbersList = [weekNumber for weekNumber in range(startWeekNumber, endWeekNumber + 1, weekStep)]
    # Начальная и конечная недели должны также присутствовать
    if startWeekNumber not in weeksNumbersList:
        weeksNumbersList.insert(0, startWeekNumber)
    if endWeekNumber not in weeksNumbersList:
        weeksNumbersList.append(endWeekNumber)
    return weeksNumbersList

def generateSchedule(weeksNumbersList, semester, startStudyYear):
    '''
    Принимает список с номерами недель, номер семестра в учебном году (False для первого
    и True для второго) и год начала учебного года в формате YY.
    Создаёт в базе данных соответствующие недели.
    В случае успеха возвращает количество созданных записей, в противном случае - None
    '''
    if not isinstance(weeksNumbersList, list) or \
       not isinstance(semester, bool) or \
       not isinstance(startStudyYear, int) or \
       not startStudyYear or not weeksNumbersList or \
       startStudyYear < 10 or startStudyYear > 35:
       return None
    # Счётчик созданных объектов
    weeksCount = 0
    for week in weeksNumbersList:
        # Проверяем существует ли уже такая неделя
        try:
            if StudyWeek.objects.get(startStudyYear=startStudyYear,
                                     number=week,
                                     semester=semester):
                # Если да, то пропускаем
                continue
        except StudyWeek.DoesNotExist:
            # Если нет, то создаём
            generatedWeek = StudyWeek(startStudyYear=startStudyYear,
                                    number=week,
                                    semester=semester)
            generatedWeek.save()
            weeksCount += 1
    return weeksCount

@login_required
def createWeeks(request):
    # Проверка, что запрос через ajax
    if not request.is_ajax():
        raise PermissionDenied
    # Проверка прав
    if not request.user.is_admin and not request.user.is_deanery:
        raise PermissionDenied
    # Способ задания требуемых недель
    by = request.GET.get('by')
    try:
        # Приводим к нужным типам
        semester = bool(int(request.GET.get('semester')))
        startStudyYear = int(request.GET.get('start_study_year'))
    except:
        return HttpResponseBadRequest()
    # Объект с ответом
    resp = {}
    if not startStudyYear:
        # Начало учебного года и семестр должны быть явно указаны
        return HttpResponseBadRequest()
    if by == 'list':
        # Способ с передочей списка всех недель
        # Разбиваем строку по запятым
        weeksNumbers = request.GET.get('weeks_numbers').split(',')
        try:
            weekNumbers = [int(week) for week in weeksNumbers]
        except:
            return HttpResponseBadRequest()
        if not weeksNumbers:
            return HttpResponseBadRequest()
        resp['result'] = generateSchedule(weeksNumbers, semester, startStudyYear)
        return JsonResponse(resp)
    elif by == 'start-end':
        # Способ по начальной и конечной неделе
        startWeekNumber = request.GET.get('start_week_number')
        endWeekNumber = request.GET.get('end_week_number')
        weekStep = request.GET.get('week_step', 1)
        if not startStudyYear or not endWeekNumber:
            return HttpResponseBadRequest()
        try:
            # Приводим к нужным типам
            startWeekNumber = int(startWeekNumber)
            endWeekNumber = int(endWeekNumber)
            weekStep = int(weekStep)
        except:
            return HttpResponseBadRequest()
        # Получаем список нужных недель
        weeksNumbers = generateWeeksNumbersBySEweeks(startWeekNumber, endWeekNumber, weekStep)
        resp['result'] = generateSchedule(weeksNumbers, semester, startStudyYear)
        return JsonResponse(resp)
    else:
        return HttpResponseBadRequest()
