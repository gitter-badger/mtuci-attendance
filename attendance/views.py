from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from attendance.models import Attendance, StudyWeek
from accounts.models import Account

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
    # Ниже ручной перебор, т.к. в bulk нет смысла
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
    ''' Создаёт требуемые недели '''
    # Проверка, что запрос через ajax
    if not request.is_ajax():
        raise PermissionDenied
    # Проверка прав
    if (not request.user.is_admin and not request.user.is_deanery) or \
        not request.user.is_active:
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

@login_required
def getWeekGroupAttendance(request):
    '''
        Принимает:
        1) start_study_year - начало учебного года (YY)
        2) semester - (0 или 1 для первого или второго соответственно)
        3) number - номер недели в семестре
    '''
    # Проверка, что запрос через ajax
    if not request.is_ajax():
        raise PermissionDenied
    # Проверка прав
    if (not request.user.is_admin and not request.user.is_deanery and not request.user.is_steward) or \
        not request.user.is_active:
        raise PermissionDenied
    try:
        semester = bool(int(request.GET.get('semester')))
        startStudyYear = int(request.GET.get('start_study_year', timezone.now().year%100))
        number = int(request.GET.get('number'))
    except:
        return HttpResponseBadRequest()
    universityGroupId = request.user.universityGroup_id
    if not number or not startStudyYear or not universityGroupId:
        return HttpResponseBadRequest()
    # Список, который будет преобразован в json и возвращен
    resp = {}
    # группа
    students = Account.objects.filter(universityGroup__id=universityGroupId)
    # посещения
    attendance = []
    # сколько объектов было создано
    createdAttCount = 0
    # Неделя
    studyWeek = StudyWeek.objects.get(startStudyYear=startStudyYear,
                                      semester=semester,
                                      number=number)
    for student in students:
        obj, created = Attendance.objects.get_or_create(studyWeek__startStudyYear=startStudyYear,
            studyWeek__semester=semester,
            studyWeek__number=number,
            student=student,
            defaults={'student': student,
                      'studyWeek': studyWeek,
                      'numberOfHours': 0})
        if obj:
            attendance.append({'student': {
                                            'id': obj.student.id,
                                            'first_name': obj.student.first_name,
                                            'last_name': obj.student.last_name
                                          },
                               'hours': obj.numberOfHours,
                               'id': obj.id})
        if created:
            createdAttCount += 1
    resp['attendance'] = sorted(attendance, key=lambda d: (d['student']['last_name']+d['student']['first_name']).lower())
    resp['created'] = createdAttCount
    return JsonResponse(resp)

@login_required
def changeAttendanceHours(request):
    '''
    Принимает id посещения и количество часов, затем записывает в бд
    и возвращает записанное число
    '''
    # Проверка, что запрос через ajax
    if not request.is_ajax():
        raise PermissionDenied
    # Проверка прав
    if (not request.user.is_admin and not request.user.is_deanery and not request.user.is_steward) or \
        not request.user.is_active:
        raise PermissionDenied
    try:
        attendanceId = int(request.GET.get('attendance_id'))
        hoursToChange = int(request.GET.get('hours', 0))
    except:
        return HttpResponseBadRequest()
    try:
        att = Attendance.objects.get(id=attendanceId)
    except Attendance.DoesNotExist:
        return HttpResponseBadRequest()
    att.numberOfHours = hoursToChange
    att.save()
    return JsonResponse({'hours': hoursToChange, 'id': attendanceId})

@login_required
def getExistingWeeks(request):
    '''Возвращает все недели в данном семестре в данном году'''
    # Проверка, что запрос через ajax
    if not request.is_ajax():
        raise PermissionDenied
    # Проверка прав
    if (not request.user.is_admin and not request.user.is_deanery and not request.user.is_steward) or \
        not request.user.is_active:
        raise PermissionDenied
    try:
        startStudyYear = int(request.GET.get('start_study_year'))
        semester = bool(int(request.GET.get('semester')))
    except:
        return HttpResponseBadRequest()
    weeks = StudyWeek.objects.filter(startStudyYear=startStudyYear, semester=semester)
    resp = {'weeks': []}
    for week in weeks:
        resp['weeks'].append({'id': week.id, 'str': week.__str__()[0:week.__str__().find('неделя')+6]})
    return JsonResponse(resp)

@login_required
def deleteWeeksById(request):
    '''Удаляет неделю по полученному id'''
    # Проверка, что запрос через ajax
    if not request.is_ajax():
        raise PermissionDenied
    # Проверка прав
    if (not request.user.is_admin and not request.user.is_deanery) or \
        not request.user.is_active:
        raise PermissionDenied
    try:
        weeksId = request.GET.get('weeks_id').split(',')
    except:
        return HttpResponseBadRequest()
    if not weeksId:
        return HttpResponseBadRequest()
    deletedWeeksCount = 0
    for weekId in weeksId:
        try:
            week = StudyWeek.objects.get(id=weekId)
            week.delete()
            deletedWeeksCount += 1
        except StudyWeek.DoesNotExist:
            continue
    return JsonResponse({'deleted': deletedWeeksCount})

def getSortingStrForStudyWeek(week):
    return str(week.startStudyYear)+str(int(week.semester))+str(week.number)

def getWeekTotalHours(week):
    return sum([att.numberOfHours for att in Attendance.objects.filter(studyWeek=week)])

@login_required
def getGlobalStatistics(request):
    # Проверка, что запрос через ajax
    if not request.is_ajax():
        raise PermissionDenied
    resp = {'labels': [], 'series': [[]]}
    # allWeeks = StudyWeek.objects.order_by('startStudyYear', 'semester', 'number')
    # Не сортируем, т.к. в модели задана сортировка по умолчанию
    allWeeks = StudyWeek.objects.all()

    for week in allWeeks:
        resp['labels'].append(getSortingStrForStudyWeek(week))
        resp['series'][0].append({
            'meta': str(int(week.semester)+1)+' семестр 20'+str(week.startStudyYear)+\
                '/20'+str(week.startStudyYear+1),
            'value': getWeekTotalHours(week) })
    return JsonResponse(resp)
