"""Модели приложения orders для магазина печатных книг."""

from django.db import models
from myShop.models import Book


class CommonInfo(models.Model):
    """
    Абстрактная модель, содержащая общие поля для других моделей:
    created и updated.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class City(CommonInfo):
    """Модель города."""
    name = models.CharField(max_length=100,
                            verbose_name="Название города", unique=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(CommonInfo):
    """Модель заказа."""

    PAYMENT_CHOICES = [
        ('при получении', 'При получении'),
        ('онлайн', 'Онлайн'),
    ]

    total_cost = models.DecimalField(max_digits=10,
                                     decimal_places=2, default=0)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default=''
    )

    city = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Город"
    )

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        """Подсчитывает общую стоимость заказа."""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Модель элемента заказа."""

    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='order_items',
                             on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """Подсчитывает стоимость данного элемента."""
        return self.price * self.quantity
