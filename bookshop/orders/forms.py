"""Форма для оформления заказа в интернет-магазине книг."""

from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """Форма для создания заказа."""

    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        label="",
    )

    class Meta:
        """Метаданные для формы."""
        model = Order
        fields = ['payment_method', 'city']
