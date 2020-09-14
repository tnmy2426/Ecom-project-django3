from django.urls import path
from .import views

app_name = 'App_Payment'

urlpatterns = [
    path('checkout/', views.CheckoutView, name='checkout_view'),
    path('pay/', views.PaymentView, name='payment_view'),
    path('status/', views.CompleteView, name='complete_view'),
    path('purchase/<val_id>/<tran_id>/', views.PurchaseView, name='purchase_view'),
    path('oeders/', views.OrderView, name='order_view'),
]
