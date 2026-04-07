"""URL конфигурации для приложения 'myShop'."""
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('search/', views.book_search, name='book_search'),
    path('<slug:genre_slug>/', views.book_list, name='book_list_by_genre'),
    path('<int:book_id>/<slug:slug>/', views.book_detail, name='book_detail'),
    path('author/<int:author_id>/', views.book_list_by_author,
         name='book_list_by_author'),
]
