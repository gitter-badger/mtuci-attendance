from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    ''' Управление кастомной моделью пользователя '''

    def create_user(self, username, password=None, **kwargs):
        "Функция создаёт пользователя"
        if not username:
            raise ValueError('Некорректный логин')
        account = self.model(
            username=username,
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
            #patronymic=kwargs.get('patronymic')
        )
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, username, password, **kwargs):
        "Функция создаёт суперпользователя"
        account = self.create_user(username, password, **kwargs)
        account.is_admin = True
        account.save()
        return account


class Account(AbstractBaseUser):
    ''' Кастомная модель пользователя, наследуемая от абстрактной стандартной '''
    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-created_at']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        # В комбинированном индексе пока необходимости нет.
        # Полнотекстовый индекс создаётся непосредственно в базе
        # index_together = []

    # Имя пользователя
    username = models.CharField('Логин',
                                max_length=40,
                                unique=True,
                                db_index=True)
    # Группа студента
    universityGroup = models.ForeignKey('UniversityGroup',
                                        verbose_name = 'Группа студента',
                                        blank=True,
                                        null=True,
                                        db_index=True)
    # Имя
    first_name = models.CharField('Имя', max_length=40, blank=True, default='', db_index=True)
    # Фамилия
    last_name = models.CharField('Фамилия', max_length=40, blank=True, default='', db_index=True)
    # Отчество
    patronymic = models.CharField('Отчество', max_length=40, blank=True, default='', db_index=True)
    # Активен?
    is_active = models.BooleanField('Активен?', default=True)
    # Является ли админом
    is_admin = models.BooleanField('', default=False)
    # Является ли старостой
    is_steward = models.BooleanField('Староста', default=False)
    # Является ли работником деканата
    is_deanery = models.BooleanField('Деканат', default=False)
    # Когда акк был создан
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    # Когда акк последний раз редактировался
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    # Указывает на manager
    objects = AccountManager()
    # Какое поле является именем пользователя
    USERNAME_FIELD = 'username'
    # Обязательные поля (имя пользователя уже обязательное)
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    def get_full_name(self):
        "Возвращает полное ФИО"
        return ' '.join([self.first_name, self.last_name, self.patronymic])

    # Название функции get_full_name
    get_full_name.short_description = 'ФИО'

    def get_short_name(self):
        "Возвращает имя"
        return self.first_name

    def __str__(self):
        "Возвращает фамилию и инициалы"
        if self.last_name and self.first_name and self.patronymic:
            return self.last_name + ' ' + self.first_name[0] + '. ' + \
               self.patronymic[0] + '.'
        elif self.last_name and self.first_name:
            return self.last_name + ' ' + self.first_name[0] + '.'
        else:
            return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class UniversityGroup(models.Model):
    ''' Модель группы студентов'''

    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-created_at']
        verbose_name = 'группа студентов'
        verbose_name_plural = 'группы студентов'

    # Название группы
    name = models.CharField('Название группы',
                            max_length=15,
                            unique=True,
                            blank=True,
                            null=False,
                            default='')
    # Когда группа была создана
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    # Когда группа последний раз редактировалась
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    def __str__(self):
        return self.name
