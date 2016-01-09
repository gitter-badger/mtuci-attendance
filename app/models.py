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
        # В комбинированном индексе пока необходимости нет.
        # Полнотекстовый индекс создаётся непосредственно в базе
        # index_together = []

    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    commit = models.CharField('Первые 7 символов хэша коммита', max_length=7, blank=True, null=True)
    changeDate = models.DateTimeField('Дата обновления', blank=True, null=True, default=now)
    description = models.TextField('Описание изменений', blank=True, null=True)

    def __str__(self):
        cutDesc = re.compile(r'\S+')
        return self.commit + ' - ' + ' '.join(cutDesc.findall(self.description)[:8]) + '...'
