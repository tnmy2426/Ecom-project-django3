from django.urls import path
from . import views

app_name = 'App_Order'

urlpatterns = [
    path('add/<pk>/', views.AddToCart, name='add_to_cart'),
    path('cart/', views.CartView, name='cart_view'),
    path('remove/<pk>', views.RemoveFromCart, name='remove_from_cart'),
    path('increase/<pk>', views.IncreaseCart, name='increase_cart'),
    path('decrease/<pk>', views.DecreaseCart, name='decrease_cart'),
]
