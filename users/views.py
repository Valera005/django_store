from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User


# Create your views here.

def login(request : WSGIRequest):

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password = password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_to=reverse("index"))

    else:
        form = UserLoginForm()


    context = {
        'form' : form,
    }

    return render(request, 'users/login.html', context)

def register(request : WSGIRequest):

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрированы")
            return HttpResponseRedirect(reverse("users:login"))

    else:
        form = UserRegistrationForm()

        context = {
        "form" : form,
        }

        return render(request, 'users/registration.html', context)

@login_required
def profile(request : WSGIRequest):

    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data= request.POST, files=request.FILES)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:profile"))

    else:
        form = UserProfileForm(instance=request.user)

    context = {
        "title" : "Store - Профиль",
        "form" : form,
        "baskets" : Basket.objects.filter(user=request.user),
    }

    return render(request, 'users/profile.html', context)

