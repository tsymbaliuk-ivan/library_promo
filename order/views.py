import datetime
from authentication.models import CustomUser
from book.models import Book
from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=True)
def order_book(request, id):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(id=request.user.id)
        book = Book.objects.get(id=id)
        today = datetime.datetime.now()
        planed_date = today + datetime.timedelta(days=14)

        if request.method == 'POST':
            form = OrderForm(request.POST)  # Bind the form with POST data
            if form.is_valid():
                order = form.save(commit=False)  # Create an Order instance but don't save it yet
                order.user = user
                order.book = book
                order.plated_end_at = planed_date
                order.save()  # Save the Order instance

                return render(request, 'order_created.html')

        else:
            form = OrderForm()

        return render(request, 'order_book.html', {'form': form})

    return redirect("login")

@ratelimit(key='ip', rate='5/m', block=True)
def close_order(request, id):
    if request.user.is_authenticated and request.user.role == 1:
        order = Order.objects.get(id=id)
        order.end_at = datetime.datetime.now()
        order.save()
        return redirect("all_orders")
    return redirect("home")

@ratelimit(key='ip', rate='5/m', block=True)
def all_orders(request):
    if request.user.is_authenticated and request.user.role == 1:
        orders = Order.objects.all()
        context = {
            'data': orders
        }
        return render(request, 'all_orders.html', context=context)
    return redirect("home")

@ratelimit(key='ip', rate='5/m', block=True)
def my_orders(request):
    if request.user.is_authenticated:
        print(request.user)
        user = CustomUser.objects.get(id=request.user.id)
        orders = Order.objects.filter(user=user)
        context = {
            'data': orders
        }
        return render(request, 'my_orders.html', context=context)
    return redirect("home")
