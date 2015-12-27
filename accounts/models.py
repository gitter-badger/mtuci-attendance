from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):

    def create_user(self, username, password=None, **kwargs):
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
        account = self.create_user(username, password, **kwargs)
        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):

    class Meta:
        # unique_together = ('steward', 'group')
        get_latest_by = 'created_at'
        ordering = ['-created_at']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    username = models.CharField('Логин',
                                max_length=40,
                                unique=True)

    # group
    first_name = models.CharField('Имя', max_length=40, blank=True, default='')
    last_name = models.CharField('Фамилия', max_length=40, blank=True, default='')
    patronymic = models.CharField('Отчество', max_length=40, blank=True, default='')
    is_active = models.BooleanField('Активен?', default=True)
    is_admin = models.BooleanField('', default=False)
    is_steward = models.BooleanField('Староста', default=False)
    is_deanery = models.BooleanField('Деканат', default=False)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)

    objects = AccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name, self.patronymic])

    get_full_name.short_description = 'ФИО'

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        if self.last_name and self.first_name and self.patronymic:
            return self.last_name + ' ' + self.first_name[0] + '. ' + \
               self.patronymic[0] + '.'
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
