from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.FloatField(null=True, blank=True, verbose_name="Цена")
    photo = models.ImageField(null=True, blank=True, upload_to="product/", verbose_name="Фото")
    manufacturer = models.CharField(null=True, blank=True, max_length=100, verbose_name="Производитель")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('buyapp:product_detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('buyapp:edit_product', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('buyapp:delete_product', kwargs={'pk': self.pk})


class ShoppingList(models.Model):
    class Status(models.TextChoices):
        ACTUAL = 'actual', 'Актуальный'
        BOUGHT = 'bought', 'Купленный'
        CANCELED = 'canceled', 'Отмененный'

    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    user_from = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_from', verbose_name="От")
    user_to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_to', null=True, blank=True, verbose_name="Купит")
    status = models.CharField(max_length=100,  choices=Status.choices, default=Status.ACTUAL, verbose_name="Статус")

    def __str__(self):
        return f'от {self.user_from.username} {self.time_created}'

    def get_absolute_url(self):
        return reverse('buyapp:shopping_list_detail', kwargs={'pk': self.pk})

class CheckCart(models.Model):
    class Status(models.TextChoices):
        ACTUAL = 'actual', 'Актуальный'
        BOUGHT = 'bought', 'Купленный'
        CANCELED = 'canceled', 'Отмененный'

    product = ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, verbose_name="Список", related_name="check_cart_list")
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.ACTUAL, verbose_name="Статус")

    def __str__(self):
        return f'Лист {self.list} Продукт {self.product.name}'

    def get_product_sum(self):
        sum = 0
        for obj in self:
            sum += obj.product.price
        return sum

