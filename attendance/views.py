import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from attendance.models import Attendance, StudyWeek
from accounts.models import Account, UniversityGroup
from django.core.cache import cache

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
    if not request.is_ajax() and not request.user.is_admin:
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
    if not request.is_ajax() and not request.user.is_admin:
        raise PermissionDenied
    # Проверка прав
    if (not request.user.is_admin and not request.user.is_deanery and \
        not request.user.is_steward) or \
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
    if not request.is_ajax() and not request.user.is_admin:
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
    if not request.is_ajax() and not request.user.is_admin:
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
    if not request.is_ajax() and not request.user.is_admin:
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

def findDictInArr(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def getStatistics(request, target):
    '''
    Стоило разнести на отдельные функции, но так строить ajax запросы проще.
    Придётся здесь пошаманить с низкоуровневым апи кэширования
    '''
    #TODO: всё-таки раскидать по функциям, хотя для того, чтобы избавиться от
    # неральных уровней вложенности
    # Проверка, что запрос через ajax
    if not request.is_ajax() and not request.user.is_admin:
        raise PermissionDenied
    if target == 'global':
        if cache.get('get_statistics_global'):
            return JsonResponse(cache.get('get_statistics_global'))
        else:
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
            cache.set('get_statistics_global', resp, 600)
            return JsonResponse(resp)
    elif target == 'user':
        userId = int(request.GET.get('id'))
        if request.user.is_authenticated() and not userId:
            userId = request.user.id
        if not userId:
            return HttpResponseBadRequest('user id is required')
        period = request.GET.get('period', 'semester')
        try:
            user = Account.objects.get(id=userId)
        except Account.DoesNotExist:
            return HttpResponseNotFound('no such user')
        if request.user.is_authenticated():
            if request.user == user or (request.user.universityGroup == user.universityGroup and
                request.user.is_steward):
                if period == 'general':
                    generalAttendance = Attendance.objects.filter(student=user)
                    resp = {'labels': [], 'series': [[]]}
                    if generalAttendance:
                        for i in range(len(generalAttendance)):
                            resp['labels'].append(i)
                            resp['series'][0].append({
                                'meta': str(int(generalAttendance[i].studyWeek.semester)+1)+\
                                        ' семестр 20'+str(generalAttendance[i].studyWeek.startStudyYear)+\
                                        '/20'+str(generalAttendance[i].studyWeek.startStudyYear+1),
                                'value': generalAttendance[i].numberOfHours })
                        return JsonResponse(resp)
                    else:
                        generalWeeks = StudyWeek.objects.all()
                        for i in range(len(generalWeeks)):
                            resp['labels'].append(i)
                            resp['series'][0].append({
                                'meta': str(int(generalWeeks[i].semester)+1)+\
                                        ' семестр 20'+str(generalWeeks[i].startStudyYear)+\
                                        '/20'+str(generalWeeks[i].startStudyYear+1),
                                'value': 0})
                        return JsonResponse(resp)
                elif period == 'semester':
                    semesterNumber = request.GET.get('number')
                    startStudyYear = request.GET.get('year')
                    if not semesterNumber or not startStudyYear:
                        today = timezone.now().date()
                        if today <= datetime.date(today.year, 12, 31) and today >= datetime.date(today.year, 9, 1):
                            # Первый семестр
                            semester = False
                        else:
                            semester = True
                        if not semester:
                            # Если 1 семестр
                            startStudyYear = today.year % 100
                        else:
                            startStudyYear = (today.year - 1) % 100
                    semesterAttendance = Attendance.objects.filter(student=user,
                                                                   studyWeek__semester=semester,
                                                                   studyWeek__startStudyYear=startStudyYear)
                    resp = {'labels': [], 'series': [[]]}
                    if semesterAttendance:
                        for i in range(len(semesterAttendance)):
                            resp['labels'].append(semesterAttendance[i].studyWeek.number)
                            resp['series'][0].append({
                                'meta': str(semesterAttendance[i].studyWeek.number) + ' неделя',
                                'value': semesterAttendance[i].numberOfHours })
                    else:
                        semesterWeeks = StudyWeek.objects.filter(semester=semester, startStudyYear=startStudyYear)
                        for week in semesterWeeks:
                            resp['labels'].append(week.number)
                            resp['series'][0].append({
                                'meta': str(week.number) + ' неделя',
                                'value': 0})
                    return JsonResponse(resp)
                else:
                    return HttpResponseBadRequest('bad period')
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
    elif target == 'semester':
        if cache.get('get_statistics_semester'):
            return JsonResponse(cache.get('get_statistics_semester'))
        else:
            startStudyYear = request.GET.get('start_study_year')
            semester = request.GET.get('semester')
            if not startStudyYear or not semester:
                today = timezone.now().date()
                if today <= datetime.date(today.year, 12, 31) and today >= datetime.date(today.year, 9, 1):
                    # Первый семестр
                    semester = False
                else:
                    semester = True
                if not semester:
                    # Если 1 семестр
                    startStudyYear = today.year % 100
                else:
                    startStudyYear = (today.year - 1) % 100
            startStudyYear = int(startStudyYear)
            semester = bool(int(semester))
            semesterWeeks = StudyWeek.objects.filter(semester=semester, startStudyYear=startStudyYear)
            if not semesterWeeks:
                return HttpResponseNotFound('no weeks in this semester')
            resp = {'labels': [], 'series': [[]]}
            for week in semesterWeeks:
                weekAttendance = Attendance.objects.filter(studyWeek=week)
                weekHours = 0
                for att in weekAttendance:
                    weekHours += att.numberOfHours
                resp['labels'].append(week.number)
                resp['series'][0].append({
                    'meta': str(week.number) + ' неделя (данный семестр)',
                    'value': weekHours})
            if not semester:
                prevSemester = True
                prevStartStudyYear = startStudyYear - 1
            else:
                prevSemester = False
                prevStartStudyYear = startStudyYear
            prevSemesterWeeks = StudyWeek.objects.filter(semester=prevSemester, startStudyYear=prevStartStudyYear)
            prevSemesterWeeksNumbers = [week.number for week in prevSemesterWeeks]
            if prevSemesterWeeks:
                resp['series'].append([])
                for weekNumber in resp['labels']:
                    if weekNumber in prevSemesterWeeksNumbers:
                        week = StudyWeek.objects.get(semester=prevSemester,
                                                       startStudyYear=prevStartStudyYear,
                                                       number=weekNumber)
                        weekAttendance = Attendance.objects.filter(studyWeek=week)
                        weekHours = 0
                        for att in weekAttendance:
                            weekHours += att.numberOfHours
                        resp['series'][1].append({
                            'meta': str(weekNumber) + ' неделя (предыдущий семестр)',
                            'value': weekHours})
                    else:
                        resp['series'][1].append({
                            'meta': str(weekNumber) + ' неделя (предыдущий семестр)',
                            'value': None})
            cache.set('get_statistics_semester', resp, 60*5)
            return JsonResponse(resp)
    elif target == 'group':
        try:
            groupId = int(request.GET.get('id'))
        except:
            return HttpResponseBadRequest('id is invalid')
        period = request.GET.get('period', 'semester')
        if not groupId:
            return HttpResponseBadRequest('group id is required')
        try:
            group = UniversityGroup.objects.get(id=groupId)
        except UniversityGroup.DoesNotExist:
            return HttpResponseNotFound('no such group')
        if request.user.is_authenticated():
            if request.user.is_steward and request.user.universityGroup == group:
                if period == 'semester':
                    semester = request.GET.get('semester')
                    startStudyYear = request.GET.get('start_study_year')
                    if not startStudyYear or not semester:
                        today = timezone.now().date()
                        if today <= datetime.date(today.year, 12, 31) and today >= datetime.date(today.year, 9, 1):
                            # Первый семестр
                            semester = False
                        else:
                            semester = True
                        if not semester:
                            # Если 1 семестр
                            startStudyYear = today.year % 100
                        else:
                            startStudyYear = (today.year - 1) % 100
                    startStudyYear = int(startStudyYear)
                    semester = bool(int(semester))
                    semesterWeeks = StudyWeek.objects.filter(semester=semester, startStudyYear=startStudyYear)
                    if not semesterWeeks:
                        return HttpResponseNotFound('no weeks in this semester')
                    resp = {'labels': [], 'series': [[]]}
                    for week in semesterWeeks:
                        weekAttendance = Attendance.objects.filter(studyWeek=week, student__universityGroup=group)
                        weekHours = 0
                        for att in weekAttendance:
                            weekHours += att.numberOfHours
                        resp['labels'].append(week.number)
                        resp['series'][0].append({
                            'meta': str(week.number) + ' неделя (данный семестр)',
                            'value': weekHours})
                    if not semester:
                        prevSemester = True
                        prevStartStudyYear = startStudyYear - 1
                    else:
                        prevSemester = False
                        prevStartStudyYear = startStudyYear
                    prevSemesterWeeks = StudyWeek.objects.filter(semester=prevSemester, startStudyYear=prevStartStudyYear)
                    prevSemesterWeeksNumbers = [week.number for week in prevSemesterWeeks]
                    if prevSemesterWeeks:
                        resp['series'].append([])
                        for weekNumber in resp['labels']:
                            if weekNumber in prevSemesterWeeksNumbers:
                                week = StudyWeek.objects.get(semester=prevSemester,
                                                             startStudyYear=prevStartStudyYear,
                                                             number=weekNumber)
                                weekAttendance = Attendance.objects.filter(studyWeek=week, student__universityGroup=group)
                                weekHours = 0
                                for att in weekAttendance:
                                    weekHours += att.numberOfHours
                                resp['series'][1].append({
                                    'meta': str(weekNumber) + ' неделя (предыдущий семестр)',
                                    'value': weekHours})
                            else:
                                resp['series'][1].append({
                                    'meta': str(weekNumber) + ' неделя (предыдущий семестр)',
                                    'value': None})
                    return JsonResponse(resp)
                elif period == 'general':
                    if cache.get('get_statistics_group_general_'+str(groupId)):
                        return JsonResponse(cache.get('get_statistics_group_general_'+str(groupId)))
                    else:
                        groupAttendance = Attendance.objects.filter(student__universityGroup=group)
                        # Записываем в нужном формате нулевые элементы
                        weeksNumbers = [str(groupAttendance[0].studyWeek.startStudyYear)+\
                                        str(int(groupAttendance[0].studyWeek.semester))+\
                                        str(groupAttendance[0].studyWeek.number)]
                        weeksCounters = [{'meta': str(int(groupAttendance[0].studyWeek.semester)+1)+\
                                                  ' семестр 20'+str(groupAttendance[0].studyWeek.startStudyYear)+\
                                                  '/20'+str(groupAttendance[0].studyWeek.startStudyYear+1),
                                          'value': groupAttendance[0].numberOfHours}]
                        # Сравниваем все остальные с предыдущим
                        for i in range(1,len(groupAttendance)):
                            # Если неделя рассматриваемого посещения та же, что и последняя,
                            # то просто приплюсовываем количество часов
                            if str(groupAttendance[i].studyWeek.startStudyYear)+\
                               str(int(groupAttendance[i].studyWeek.semester))+\
                               str(groupAttendance[i].studyWeek.number) == weeksNumbers[-1]:
                               weeksCounters[-1]['value'] += groupAttendance[i].numberOfHours
                            else:
                                # Иначе создаём новую запись
                                weeksNumbers.append(str(groupAttendance[i].studyWeek.startStudyYear)+\
                                                    str(int(groupAttendance[i].studyWeek.semester))+\
                                                    str(groupAttendance[i].studyWeek.number))
                                weeksCounters.append({'meta': str(int(groupAttendance[i].studyWeek.semester)+1)+\
                                                              ' семестр 20'+str(groupAttendance[i].studyWeek.startStudyYear)+\
                                                              '/20'+str(groupAttendance[i].studyWeek.startStudyYear+1),
                                                      'value': groupAttendance[i].numberOfHours})
                        resp = {'labels':weeksNumbers, 'series': [weeksCounters]}
                        cache.set('get_statistics_group_general_'+str(groupId), resp, 60*5)
                        return JsonResponse(resp)
                else:
                    return HttpResponseBadRequest('invalid period')
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
    elif target == 'top_5_attendance':
        # Для топа на странице attendance
        if cache.get('get_statistics_top_5_attendance'):
            return JsonResponse(cache.get('get_statistics_top_5_attendance'))
        else:
            allAtt = Attendance.objects.all()
            studentsHours = []
            groupsHours = []
            for att in allAtt:
                if att.student:
                    if any(d['name'] == att.student.last_name+' '+att.student.first_name for d in studentsHours):
                        studentsHours[findDictInArr(studentsHours,'name',att.student.last_name+' '+att.student.first_name)]['hours'] += att.numberOfHours
                    else:
                        studentsHours.append({'name':att.student.last_name+' '+att.student.first_name, 'hours':att.numberOfHours})
                if att.student.universityGroup:
                    if any(d['name'] == att.student.universityGroup.name for d in groupsHours):
                        groupsHours[findDictInArr(groupsHours,'name',att.student.universityGroup.name)]['hours'] += att.numberOfHours
                    else:
                        groupsHours.append({'name':att.student.universityGroup.name, 'hours':att.numberOfHours})
                studentsHours = sorted(studentsHours, key=lambda d: d['hours'], reverse=True)
                groupsHours = sorted(groupsHours, key=lambda d: d['hours'], reverse=True)
            resp = {'students':studentsHours[:5],'groups':groupsHours[:5]}
            cache.set('get_statistics_top_5_attendance', resp, 60*30)
            return JsonResponse(resp)
    else:
        return HttpResponseBadRequest('bad target')

def attendance(request):
    return render(request, 'attendance/attendance.html', {})
