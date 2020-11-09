from django.contrib import admin
from .models import Rubric, Article
#  from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin


# admin.site.register(Rubric, MPTTModelAdmin)  # MPTTModelAdmin нужно для оформления админки
admin.site.register(Article)

admin.site.register(
    Rubric,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)  # Тоже оформление админки, но более удобное
