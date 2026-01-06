from django.contrib import admin
from django.utils.safestring import mark_safe

import content
from content.models import Category, Content, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_display_links = ('id', 'name')
    save_on_top = True



@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'status', 'stars_rating', 'picture_print', 'user', 'time_created', 'time_updated')
    list_display_links = ('id',)
    search_fields = ('user__username', 'category__name')
    save_on_top = True

    @admin.display(description="Изображение")
    def picture_print(self, content: Content):
        if content.picture:
            return mark_safe(f'<img src="{content.picture.url}" height="50" />')
        else:
            return 'Нет изображения'

    @admin.display(description="Рейтинг")
    def stars_rating(self, content: Content):
        return content.stars_display()

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'user', 'time_created', 'time_updated')

