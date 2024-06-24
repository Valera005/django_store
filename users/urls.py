from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from users.views import (EmailVerificationView, UserLoginView, UserProfileView,
                         UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view(next_page=reverse_lazy("users:login"))), name='logout'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='email_verification'),

]
