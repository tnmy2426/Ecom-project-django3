from django.urls import path
from .import views

app_name = 'App_Login'

urlpatterns = [
    path('signup/', views.SignupView, name='signup_view'),
    path('login/', views.LoginView, name='login_view'),
    path('logout/', views.LogoutView, name='logout_view'),
    path('profile/', views.ProfileView, name='profile_view'),
]
