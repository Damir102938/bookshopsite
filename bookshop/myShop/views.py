"""Представления для приложения 'myShop'."""
from django.shortcuts import render, get_object_or_404, redirect
from .models import Genre, Book, Author
from cart.forms import CartAddBookForm
from django.utils.timezone import now
from django.db.models import Q


def get_published_books():
    """Фильтрация книг, которые доступны и не скрыты."""
    current_time = now()
    return Book.objects.filter(
        available=True,
        created__lte=current_time,
        hidden=False
    )


def book_search(request):
    """Поиск книг по названию, автору или жанру."""
    query = request.GET.get('query', '').strip()
    if query:
        try:
            genre = Genre.objects.get(name__iexact=query)
            return redirect(genre.get_absolute_url())
        except Genre.DoesNotExist:
            pass

        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query)
        )
    else:
        books = []

    return render(request, 'shop/book/search.html', {
        'query': query,
        'books': books
    })


def book_list(request, genre_slug=None):
    """Список книг, с возможностью фильтрации по жанру."""
    genres = Genre.objects.all()
    books = Book.objects.filter(available=True, hidden=False)
    selected_genre = None

    if genre_slug:
        selected_genre = get_object_or_404(Genre, slug=genre_slug)
        books = books.filter(genres=selected_genre)

    return render(request, 'shop/book/list.html', {
        'books': books,
        'genres': genres,
        'selected_genre': selected_genre
    })


def book_detail(request, book_id, slug):
    """Информация о книге."""
    book = get_object_or_404(
        Book,
        id=book_id,
        slug=slug,
        available=True
    )
    cart_book_form = CartAddBookForm()
    return render(request,
                  'shop/book/detail.html',
                  {'book': book,
                   'cart_book_form': cart_book_form})


def book_list_by_author(request, author_id):
    """Список книг конкретного автора."""
    author = get_object_or_404(Author, id=author_id)
    books = get_published_books().filter(author=author)
    return render(request,
                  'shop/book/list_by_author.html',
                  {'author': author,
                   'books': books})


def csrf_failure(request, reason=''):
    """403 — CSRF ошибка."""
    return render(request, '403csrf.html', status=403)


def page_not_found(request, exception):
    """404 — страница не найдена."""
    return render(request, '404.html', status=404)


def server_error(request):
    """500 — внутренняя ошибка сервера."""
    return render(request, '500.html', status=500)
