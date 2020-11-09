from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Для того чтобы появился СКЕдитор
class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # пер-ая автоматически пишет url из названия тайтла
    form = PostAdminForm  # Связываем с виджетом для редактора контента
    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'get_photo')  # какие столбцы будут видны
    list_display_links = ('id', 'title')  # на какие строки ссылка
    search_fields = ('title',)  # по чему можно искать
    list_filter = ('category', 'tags')  # боковая панель фильтрации
    readonly_fields = ('views', 'created_at', 'get_photo')  # поля только для чтения которые нельзя менять
    fields = ('title', 'slug', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at',)  # при редактовании какие поля видны и в каком порядке

    def get_photo(self, obj):
        if obj.photo:  # если есть фото возвращаем штмл-строку для его показа, если нет то No photo
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return 'No photo'

    get_photo.short_description = 'Фото'  # короткое описание столбца для админки, так как функции нет в модели


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
