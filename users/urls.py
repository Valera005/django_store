from django.urls import path

from users.views import profile, register, login

app_name = 'users'

urlpatterns = [
    path('register/', register, name='registration'),
    path('profile/', profile, name='profile'),
    path('login/', login, name='login'),

]