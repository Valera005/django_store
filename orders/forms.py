from django import forms
from django.forms import ModelForm

from orders.models import Order


class OrderForm(ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Иван"}))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Иванов"}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control", "placeholder": "you@example.com"}))

    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Россия, Москва, ул. Мира, дом 6"}))

    class Meta:
        model = Order
        fields = ('first_name', "last_name", "email", "address")
