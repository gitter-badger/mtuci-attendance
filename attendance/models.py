from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator

class StudyWeek(models.Model):
    ''' Модель учебной недели '''
    class Meta:
        # Каждому семестру в каждом году может соответствовать только одна
        # неделя с определенным номером
        unique_together = ('startStudyYear', 'number', 'semester')
        get_latest_by = 'created_at'
        ordering = ['startStudyYear', 'number']
        verbose_name = 'учебная неделя'
        verbose_name_plural = 'учебные недели'

    # Номер календарного года, с которого начался учебный год. (состоит из двух цифр)
    startStudyYear = models.PositiveSmallIntegerField('Год начала учебного года',
                                                      help_text='Две последние цифры в формате <em>YY</em>',
                                                      null=False,
                                                      blank=False,
                                                      default=now().year % 100,
                                                      validators=[
                                                        MinValueValidator(10,
                                                            message='Минимальное значение 10'),
                                                        MaxValueValidator(35,
                                                            message='Слишком большой номер года')
                                                      ])
    # Номер недели в семестре начиная с единицы
    number = models.PositiveSmallIntegerField('Номер в семестре',
                                              null=False,
                                              blank=False,
                                              default=1,
                                              validators=[
                                                MinValueValidator(1,
                                                    message='Отсчёт начинается с единицы'),
                                                MaxValueValidator(25,
                                                    message='Слишком большой номер недели')
                                              ])
    SEMESTER_CHOICES = (
        (False, 'Первый семестр'),
        (True, 'Второй семестр')
    )
    # 0 - если первый семестр, 1 - если второй семестр (в учебном году, не в календарном!)
    semester = models.BooleanField('Номер семестра',
                                   blank=False,
                                   null=False,
                                   default=False,
                                   choices=SEMESTER_CHOICES,
                                   help_text='Номер семестра в учебном году, не в календарном')
    # Когда неделя была создана
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    # Когда неделя последний раз редактировалась
    updated_at = models.DateTimeField('Обновлен', auto_now=True)

    def __str__(self):
        "Возвращает читабельное название недели"
        return str(self.number) + 'ая неделя ' + str(int(self.semester) + 1) + \
            + 'го семестра 20' + str(self.startStudyYear) + '/20' + \
            str(self.startStudyYear + 1)


class Attendance(models.Model):
    ''' Модель посещений. Информация: какой студент сколько часов посетил на определенной неделе '''
    class Meta:
        # Каждому студенту соответствует только одна неделя
        unique_together = ('student', 'studyWeek')
        get_latest_by = 'created_at'
        ordering = ['-studyWeek', '-created_at']
        verbose_name = 'посещение'
        verbose_name_plural = 'посещения'
    # Кто
    student = models.ForeignKey('accounts.Account',
                                verbose_name = 'Студент',
                                blank=True,
                                null=True,
                                help_text='Студент, который посещал занятия')
    # Когда
    studyWeek = models.ForeignKey('StudyWeek',
                                  verbose_name = 'Неделя',
                                  blank=True,
                                  null=True,
                                  help_text='Учебная неделя, для которой указывается посещение')
    # Сколько часов
    numberOfHours = models.PositiveSmallIntegerField('Количество часов',
                                                     null=False,
                                                     blank=False,
                                                     default=0,
                                                     validators=[
                                                        MinValueValidator(0,
                                                             message='Не может быть меньше нуля'),
                                                        MaxValueValidator(250,
                                                             message='Слишком большое число')
                                                                ])
    # Когда посещение было создано
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    # Когда посещение последний раз редактировалось
    updated_at = models.DateTimeField('Обновлен', auto_now=True)

    def __str__(self):
        return student.__str() + ' | ' + studyWeek.__str__()
