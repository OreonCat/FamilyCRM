from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name


class Content(models.Model):

    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Не начат'
        IN_PROGRESS = 'ip_progress', 'В процессе'
        COMPLETED = 'conpleted', 'Завершен'

    name = models.CharField(max_length=100, verbose_name="Название")
    status = models.CharField(max_length=100,  choices=Status.choices, default=Status.NOT_STARTED, verbose_name="Статус")
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Рейтинг")
    picture = models.ImageField(upload_to="content/pictures", null=True, blank=True, default=None, verbose_name="Изображение")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="content", verbose_name="Категория")
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name="Пользователь")
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('content-detail', kwargs={'pk': self.pk})

    def stars_display(self):
        return '★' * self.rating + '☆' * (5 - self.rating)


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name="Контент", related_name="comments")
    message = models.TextField(verbose_name="Сообщение")
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def can_edit(self, user, content):
        return user == self.user and self.content == content

    def get_edit_url(self):
        return f"{reverse('content-detail', kwargs={'pk': self.content.id})}?edit_comment={self.pk}"

    def get_delete_url(self):
        return reverse('delete-comment-content', kwargs={'pk': self.pk})