from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from django.db.models import F


class Home(ListView):  # Этот класс возвращает список, исп-ся вместо index
    model = Post  # Список из какой модели конкретно возвращает класс
    template_name = 'blog/index.html'  # Какой шаблон вызывает класс, этот класс связывается с этой стр.
    context_object_name = 'posts'  # Вместо object_list можно использовать posts в штмл-документах для вызова класса
    paginate_by = 4  # кол-во постов на стр для пагинации
    allow_empty = False  # При запросе несуществующей категории ошибка 404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Classic Blog Design'  # Тайтл index.html теперь называется так
        return context


class PostsByCategory(ListView):
    # model = Post - не нужно, так как в ф-ции get_queryset мы обращаемся к классу
    template_name = 'blog/index.html'  # делаем такой же как классе Home, или можно другой, но стр придется делать отдельно
    context_object_name = 'posts'  # делаем такой же как классе Home, чтобы на той же странице выдавало уже отфильтрованный список статей
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):  # Этот метод выдает список из объектов, которые фильтруются соответственно
        # обращаемся к классу Post, но фильтруем по Category, так как классы связаны
        return Post.objects.filter(category__slug=self.kwargs['slug'])  # kwargs['slug'] равен <str:slug> из url

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1  # Класс F сравнивает текущее значение и добавляет к нему 1
        self.object.save()  # Необходимо сохранить результат, но он будет не числом, а выражением, поэтому необходимо обновить БД
        self.object.refresh_from_db()  # Обновляем БД, иначе будет выражение F(views) + Value(1)
        context['title'] = Post.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


class Search(ListView):  # Класс для поиска
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        # request - данные пришли от пользователя, GET (массив) - method="get" в штмл,
        # get - самая ф-ция изъятия, 's' - по ключу name="s" в штмл (то есть указываем имя input и передаем его сюда, чтобы знать что искать)
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"  # Строка поискового запроса для пагинации: s=поисковый+запрос&
        return context

