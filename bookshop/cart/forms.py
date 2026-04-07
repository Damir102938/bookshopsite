"""Формы для приложения 'cart'."""
from django import forms

# Количество книг, которое пользователь может добавить за один раз
BOOK_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddBookForm(forms.Form):
    """Форма для добавления книги в корзину."""

    quantity = forms.TypedChoiceField(
        choices=BOOK_QUANTITY_CHOICES,
        coerce=int
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
