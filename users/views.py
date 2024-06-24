
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User

# Create your views here.

class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = "Store - Auth"

    def get_success_url(self):
        user = User.objects.get(username=self.request.POST['username'])
        return reverse_lazy('users:profile', args=[user.id])


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")
    success_message = "Вы успешно зарегистрированы"
    title = "Store - Регистрация"


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    title = "Store - Личный кабинет"

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.object.id])

    # def get_context_data(self, **kwargs):
    #     context = super(UserProfileView, self).get_context_data()
    #     context["baskets"] = Basket.objects.filter(user=self.object)
    #     return context


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Store - Email verify"
    template_name = "users/email_verification.html"

    def get(self, request, *args, **kwargs):
        code = kwargs.get("code")
        user = User.objects.get(email=kwargs.get("email"))
        email_verifications = EmailVerification.objects.filter(user=user, code=code)

        if email_verifications.exists() and email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("index"))


# def login(request : WSGIRequest):
#
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#
#             user = auth.authenticate(username=username, password = password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(redirect_to=reverse("index"))
#
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'form' : form,
#     }
#
#     return render(request, 'users/login.html', context)


# def register(request : WSGIRequest):
#
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Вы успешно зарегистрированы")
#             return HttpResponseRedirect(reverse("users:login"))
#
#     else:
#         form = UserRegistrationForm()
#
#         context = {
#         "form" : form,
#         }
#
#         return render(request, 'users/registration.html', context)


# @login_required
# def profile(request : WSGIRequest):
#
#     if request.method == "POST":
#         form = UserProfileForm(instance=request.user, data= request.POST, files=request.FILES)
#
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("users:profile"))
#
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     context = {
#         "title" : "Store - Профиль",
#         "form" : form,
#         "baskets" : Basket.objects.filter(user=request.user),
#     }
#
#     return render(request, 'users/profile.html', context)


# @login_required
# def user_logout(request: WSGIRequest):
#     logout(request)
#     return HttpResponseRedirect(redirect_to=reverse("users:login"))
