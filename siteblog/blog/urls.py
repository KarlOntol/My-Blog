from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),  # Вместо ф-ции index используем класс Home и ф-цию для вывода as_view
    path('category/<str:slug>', PostsByCategory.as_view(), name='category'),  # Когда мы попадаем на эту страницу, выз-ся этот класс
    path('tag/<str:slug>', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>', GetPost.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
]
