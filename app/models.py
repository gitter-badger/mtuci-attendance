from django.db import models
from django.utils.timezone import now
import re

class LastChange(models.Model):
    '''
    Последние изменения на сайте
    '''
    class Meta:
        get_latest_by = 'changeDate'
        ordering = ['-changeDate', '-created_at']
        verbose_name = 'обновление'
        verbose_name_plural = 'обновления'

    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    commit = models.CharField('Первые 7 символов хэша коммита', max_length=7, blank=True, null=True)
    changeDate = models.DateTimeField('Дата обновления', blank=True, null=True, default=now)
    description = models.TextField('Описание изменений', max_length=255, blank=True, null=True)

    def __str__(self):
        cutDesc = re.compile(r'\S+')
        return self.commit + ' - ' + ' '.join(cutDesc.findall(self.description)[:8]) + '...'

class Plan(models.Model):
    '''
    Что планируется сделать
    '''
    class Meta:
        get_latest_by = 'created_at'
        ordering = ['created_at']
        verbose_name = 'план'
        verbose_name_plural = 'планы'

    is_complited = models.BooleanField('Выполнено?', default=False)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    description = models.TextField('Описание пункта плана', max_length=255, blank=True, null=True)

    def __str__(self):
        cutDesc = re.compile(r'\S+')
        return ' '.join(cutDesc.findall(self.description)[:8]) + '...'
