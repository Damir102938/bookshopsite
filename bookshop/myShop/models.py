"""Модели приложения myShop."""
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    """Модель для жанров книг."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:book_list_by_genre', args=[self.slug])


class Author(models.Model):
    """Модель для авторов книг."""
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель для книг."""
    genres = models.ManyToManyField(Genre, related_name='books')
    author = models.ForeignKey(Author, related_name='books',
                               on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='books/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    pages = models.PositiveIntegerField(null=True,
                                        blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['title']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:book_detail', args=[self.id, self.slug])
