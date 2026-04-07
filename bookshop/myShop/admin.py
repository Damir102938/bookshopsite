"""
Этот модуль содержит регистрацию моделей в Django Admin.

Здесь указаны настройки отображения и поиска для моделей 'Genre', 'Author'
и 'Book'.
"""
from django.contrib import admin
from .models import Genre, Book, Author


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'display_genres',
                    'price', 'pages', 'created', 'updated']
    list_filter = ['genres', 'created', 'updated']
    search_fields = ['title', 'author__name']
    prepopulated_fields = {'slug': ('title',)}

    def display_genres(self, obj):
        """Показываем все жанры через запятую в списке книг админки."""
        return ", ".join([genre.name for genre in obj.genres.all()])
    display_genres.short_description = 'Genres'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
