from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse

# models
from .models import BillingAddress
from App_Order.models import Order, Cart

#forms
from .forms import BillingForm

# for authentication 
from django.contrib.auth.decorators import login_required

#for payment
import requests
import socket
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

#messages
from django.contrib import messages

# Create your views here.

@login_required
def CheckoutView(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == "POST":
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, "Shipping Address Saved Successfully")

    order_exist = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_exist[0].orderitems.all()
    order_total = order_exist[0].get_totals()
    return render(request, 'App_Payment/checkout_page.html', {'form':form, 'order_items':order_items, 'order_total':order_total, 'saved_address':saved_address})

@login_required
def PaymentView(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request, "Complete shipping address")
        return redirect('App_Payment:checkout_view')

    if not request.user.profile.is_fully_filled():
        messages.info(request, "Please complete your profile information")
        return redirect('App_Login:profile_view')
        
    # for payment section
    store_id = 'xyz5f3e8e1ac0821'
    API_key = 'xyz5f3e8e1ac0821@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)

    status_url = request.build_absolute_uri(reverse('App_Payment:complete_view'))
    mypayment.set_urls(
        success_url=status_url, 
        fail_url=status_url, 
        cancel_url=status_url, 
        ipn_url=status_url
    )

    order_exist = Order.objects.filter(user=request.user, ordered=False)
    order_exist = order_exist[0]
    order_items = order_exist.orderitems.all()
    order_item_count = order_exist.orderitems.count()
    order_total = order_exist.get_totals()
    mypayment.set_product_integration(
        total_amount=Decimal(order_total), 
        currency='BDT', 
        product_category='Mixed', 
        product_name=order_items, 
        num_of_item=order_item_count, 
        shipping_method='Courier', 
        product_profile='None'
    )
    
    current_user = request.user
    mypayment.set_customer_info(
        name=current_user.profile.full_name, 
        email=current_user.email, 
        address1=current_user.profile.address_one, 
        address2=current_user.profile.address_one, 
        city=current_user.profile.city, 
        postcode=current_user.profile.zipcode, 
        country=current_user.profile.country, 
        phone=current_user.profile.phone
    )

    mypayment.set_shipping_info(
        shipping_to=current_user.profile.full_name, 
        address=saved_address.address, 
        city=saved_address.city, 
        postcode=saved_address.zipcode, 
        country=saved_address.country
    )

    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def CompleteView(request):
    if request.method == "POST" or request.method == "post":
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            tran_id = payment_data['tran_id']
            val_id = payment_data['val_id']
            bank_tran_id = payment_data['bank_tran_id']
            messages.success(request,"Your payment completed successfully")
            return HttpResponseRedirect(reverse('App_Payment:purchase_view', kwargs={
                'val_id':val_id, 'tran_id':tran_id
            }))
        elif status == 'FAILED':
            messages.warning(request, "Your payment failed! Please try again.")
    return render(request, 'App_Payment/complete_page.html', {})

@login_required
def PurchaseView(request, val_id, tran_id):
    # making ordered value True
    order_exist = Order.objects.filter(user=request.user, ordered=False)
    order = order_exist[0]
    orderId = tran_id
    order.ordered = True
    order.orderId = orderId
    order.paymentId = val_id
    order.save()

    #making purchased value True
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse('App_Shop:home'))

@login_required
def OrderView(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {'orders':orders}
    except:
        messages.warning(request, "You don't have any order")
        return redirect('App_Shop:home')

    return render(request, 'App_Payment/order_page.html', context)