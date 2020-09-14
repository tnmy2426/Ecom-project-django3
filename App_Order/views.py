from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Order
from App_Shop.models import Product

#for authentication
from django.contrib.auth.decorators import login_required

#messages
from django.contrib import messages


# Create your views here.

@login_required
def AddToCart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_exist = Order.objects.filter(user=request.user, ordered=False)
    if order_exist.exists():
        order = order_exist[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, 'Item quantity updated')
            return redirect('App_Shop:home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "Item added to your cart")
            return redirect('App_Shop:home')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, 'Item added to your Cart')
        return redirect('App_Shop:home')

@login_required
def CartView(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'App_Order/cart_page.html', {"order":order, "carts":carts})
    else:
        messages.warning(request, "You don't have any item in your Cart")
        return redirect('App_Shop:home')

@login_required
def RemoveFromCart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_exist = Order.objects.filter(user=request.user, ordered=False)
    if order_exist.exists():
        order = order_exist[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "Item removed from your cart")
            return redirect('App_Order:cart_view')

        else:
            messages.warning(request, "Item not in your cart")
            return redirect('App_Shop:home')
    else:
        messages.warning(request, "You don't have any order")
        return redirect('App_Shop:home')


@login_required
def IncreaseCart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_exist = Order.objects.filter(user=request.user, ordered=False)
    if order_exist.exists():
        order = order_exist[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.success(request, f"{ item.product_name } quantity increased")
                return redirect('App_Order:cart_view')
        else:
            messages.warning(request, f"{item.product_name} is not in your cart.")
    else:
        messages.warning(request, "You don't have any order")
        return redirect('App_Shop:home')

@login_required
def DecreaseCart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_exist = Order.objects.filter(user=request.user, ordered=False)
    if order_exist.exists():
        order = order_exist[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.warning(request, f"{ item.product_name } quantity decreased")
                return redirect('App_Order:cart_view')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{ item.product_name } removed from your cart")
                return redirect('App_Order:cart_view')
        else:
            messages.warning(request, f"{ item.product_name } is not in your cart.")
    else:
        messages.warning(request, "You don't have any order")