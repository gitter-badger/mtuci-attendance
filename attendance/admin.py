from django.contrib import admin
from attendance.models import StudyWeek, Attendance


class StudyWeekAdmin(admin.ModelAdmin):
    fields = ['startStudyYear', 'semester', 'number']
    list_display = ('__str__',)
    list_display_links = ('__str__',)
    list_filter = ['startStudyYear', 'semester', 'number']
    ordering = ['-startStudyYear', '-semester', '-number']


class AttendanceAdmin(admin.ModelAdmin):
    fields = ['student', 'studyWeek', 'numberOfHours']
    list_display = ('student', 'studyWeek', 'numberOfHours')
    list_display_links = ('student', 'studyWeek', 'numberOfHours')
    list_filter = ['numberOfHours',
                   'student__universityGroup__name',
                   'studyWeek__semester',
                   'studyWeek__startStudyYear',
                   'studyWeek__number']
    ordering = ['-studyWeek']
    search_fields = ['student__last_name',
                     'student__first_name',
                     'student__universityGroup__name',
                     'student__patronymic']


admin.site.register(StudyWeek, StudyWeekAdmin)
admin.site.register(Attendance, AttendanceAdmin)
