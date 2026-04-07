"""Представления для приложения 'orders' в магазине книг."""

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.utils.timezone import now
import random


def order_create(request):
    """Создание заказа из корзины."""
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Создаём заказ
            order = form.save(commit=False)
            order.payment_method = form.cleaned_data['payment_method']

            # Общая стоимость заказа из корзины
            order.total_cost = sum(item['price'] * item['quantity']
                                   for item in cart)
            order.save()

            # Создаём элементы заказа
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    book=item['book'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Очистка корзины и сохранение ID заказа в сессии
            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('orders:order_success'))

    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


def order_success(request):
    """Отображение чека после успешного оформления заказа."""
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)

    receipt_data = {
        'order_id': order.id,
        'total_cost': order.total_cost,
        'order_items': order.items.all(),
        'order_city': order.city,
        'order_time': now().strftime('%d-%m-%Y %H:%M:%S'),
        'transport_company': random.choice(
            ['Transport Company 1', 'Transport Company 2',
             'Transport Company 3', 'Transport Company 4',
             'Transport Company 5']),
        'payment_method': order.payment_method,
    }

    return render(request, 'orders/order/success.html', receipt_data)
