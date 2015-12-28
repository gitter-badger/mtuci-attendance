from django.shortcuts import render
from attendance.models import StudyWeek

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
    В случае успеха возвращает True, в противном случае - False
    '''
    if not isinstance(weeksNumbersList, list) or \
       not isinstance(semester, bool) or \
       not isinstance(startStudyYear, int) or \
       not startStudyYear or not weeksNumbersList or \
       startStudyYear < 10 or startStudyYear > 35:
       return False
    # Список с объектами недель
    weeksList = []
    for week in weeksNumbersList:
        weeksList.append(StudyWeek(startStudyYear=startStudyYear,
                                   number=week,
                                   semester=semester))
    # Сохраняем все объекты в БД (максимум 300 за запрос)
    StudyWeek.objects.bulk_create(weeksList, 300)
