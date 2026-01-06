from django.contrib import admin
from django.utils import timezone

from .models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'deadline', 'time_created', 'time_updated', 'deadline_over_display', 'now_time')

    @admin.display(description='Истек')
    def deadline_over_display(self, task: Task):
        return task.deadline_is_over()

    @admin.display(description="Нынешнее время")
    def now_time(self, task: Task):
        return timezone.now()