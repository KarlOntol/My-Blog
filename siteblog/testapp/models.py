from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Rubric(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    # 'self' нужен чтобы ссылаться на ту же самую модель (то есть parent будет ссылаться на id своего экземпляра)
    # 'related_name' - в кач-ве ссылки исп-ся название 'children'
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        return reverse('rubric', kwargs={"pk": self.pk})


class Article(models.Model):
    name = models.CharField(max_length=50)
    category = TreeForeignKey(Rubric, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
