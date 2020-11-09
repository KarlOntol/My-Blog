from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)  # слаг это формирование url читабельным текстом

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # нужно чтобы строить ссылкку category/имя_категории на каждую категорию
        return reverse('category', kwargs={"slug": self.slug})  # это просто ссылка, саму стр добавляем в PostsByCategory во views.py

    class Meta:  # Мета нужен для визуализации админки
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']  # Как будет сортироваться столбец


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # нужно чтобы строить ссылкку post/имя_категории на каждую категорию
        return reverse('tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # нужно чтобы строить ссылкку post/имя_категории на каждую категорию
        return reverse('post', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['created_at']
