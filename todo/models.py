from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _

from enum import Enum


class Mark(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,
                            verbose_name=_('Название'))

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
        db_table = 'db_mark'


class TaskStatus(Enum):
    PROGRESS = _("В процессе")
    COMPLETED = _("Выполнено")

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150,
                             verbose_name=_('Задача'))
    description = models.TextField(blank=True,
                                   verbose_name=_('Описание'))
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"),
                               verbose_name=_('Создано'))
    deadline = models.DateField(default=timezone.now().strftime("%Y-%m-%d"),
                                verbose_name=_('Дедлайн'))
    mark = models.ForeignKey(Mark,
                             on_delete=models.CASCADE,
                             default="general",
                             verbose_name=_('Метка'))
    status = models.CharField(max_length=15,
                              choices=TaskStatus.choices(),
                              default=TaskStatus.PROGRESS,
                              verbose_name='Статус')

    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])

    class Meta:
        ordering = ["-created"]
        verbose_name = 'Задание'
        verbose_name_plural = 'Задание'
        db_table = 'db_task'
