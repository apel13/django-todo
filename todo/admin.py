from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from . import models


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "deadline")


class MarkAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(models.Mark, MarkAdmin)
admin.site.register(models.Task, TaskAdmin)
