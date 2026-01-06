from django.contrib import admin

from buyapp.models import Product, ShoppingList, CheckCart


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "manufacturer")

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("id", "time_created", "time_updated", "user_from", "user_to", "status")

@admin.register(CheckCart)
class CheckCartAdmin(admin.ModelAdmin):
    list_display = ("id", "list", "product", "status")