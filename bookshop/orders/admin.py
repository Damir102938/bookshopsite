"""
Регистрация моделей заказа в Django Admin.

Настройки отображения и поиска для моделей Order, OrderItem и DiscountCard.
"""

from django.contrib import admin
from .models import City, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Встраиваемый интерфейс для элементов заказа (OrderItem)."""

    model = OrderItem
    raw_id_fields = ['book']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Order."""

    list_display = ['id', 'created', 'updated', 'payment_method']
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
