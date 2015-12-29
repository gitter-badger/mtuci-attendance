from django.contrib import admin
from attendance.models import StudyWeek, Attendance


class StudyWeekAdmin(admin.ModelAdmin):
    fields = ['startStudyYear', 'semester', 'number']
    list_display = ('__str__',)
    list_display_links = ('__str__',)
    list_filter = ['startStudyYear', 'semester', 'number']
    ordering = ['-startStudyYear', '-semester', '-number']


admin.site.register(StudyWeek, StudyWeekAdmin)
admin.site.register(Attendance)
