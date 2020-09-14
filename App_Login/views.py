from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.urls import reverse

#Authentication 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# forms and models
from .models import Profile
from .forms import ProfileForm, SignupForm

# messages 
from django.contrib import messages


# Create your views here.

def SignupView(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Created Successfully.')
            return HttpResponseRedirect(reverse('App_Login:login_view'))
    return render(request, 'App_Login/signup_page.html', {'form':form})

def LoginView(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Shop:home'))
            else:
                messages.error(request, 'Username or Password incorrect')
    return render(request, 'App_Login/login_page.html', {'form':form})

@login_required
def LogoutView(request):
    logout(request)
    messages.warning(request, 'Logout successfull.')
    return redirect('App_Shop:home')

@login_required
def ProfileView(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Information saved.')
            form = ProfileForm(instance=profile)
    return render(request, 'App_Login/profile_page.html', {'form':form})