# Здесь пишем теги для менюшки. 2-ая ступень, пред. menu_tpl след. _header

from django import template
from blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/menu_tpl.html')  # Из какого штмд-док берем визуальную модель для её формирования
def show_menu(menu_class='menu'):  # Мы называем menu_class тем именем класса который указан в ксс коде изначально для сохранения стиля
    categories = Category.objects.all()  # берем данные из Категории
    return {"categories": categories, "menu_class": menu_class}  # Ключи это пер-ые из штмл-кода, значения - пер-ые из menu.py

# Эта функция берет визуал из menu_tpl.html и наполняет его данными из модели с соответствующим стилем.
# Это полноценная ф-ция для вставки в штмл-документ - {% show_menu %}
