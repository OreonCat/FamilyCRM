from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Task(models.Model):

    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В процессе'
        COMPLETED = 'completed', 'Завершено'

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    status = models.CharField(choices=Status.choices, default=Status.NEW, max_length=100, verbose_name="Статус")
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.name

    def deadline_is_over(self):
        return self.deadline is not None and self.deadline < timezone.now() and self.status != 'completed'

    def get_absolute_url(self):
        return reverse('tasks:task_detail', kwargs={'pk': self.pk})


