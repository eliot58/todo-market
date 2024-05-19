import re
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password


class RegisterForm(forms.Form):
    fullName = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder": "Введите ФИО", "class": "input-field", "id": "fullName"}))
    ch = [
        ("", "Выберите специализацию"),
        ("B", "Покупатель"),
        ("P", "Поставщик")
    ]
    spec = forms.ChoiceField(choices=ch, label="", widget=forms.Select(attrs={"class": "input-field"}))
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={"placeholder": "Введите почту", "class": "input-field", "id": "email"}))
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder": "Введите номер телефона", "class": "input-field", "id": "phone"}))

    
    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        spec = self.cleaned_data["spec"]
        regx = re.match(r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$", phone)
        try:
            regx.start()
        except AttributeError:
            raise ValidationError("Введите правильный номер (+79855310868)")
        if spec == "P":
            try:
                Provider.objects.get(phone=phone)
            except Provider.DoesNotExist:
                pass
            else:
                raise ValidationError("Пользователь с таким номером уже есть")
        else:
            try:
                Buyer.objects.get(phone=phone)
            except Buyer.DoesNotExist:
                pass
            else:
                raise ValidationError("Пользователь с таким номером уже есть")
        return phone
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(username=email)
        except User.DoesNotExist:
            pass
        else:
            raise ValidationError("Пользователь с такой почтой уже есть")
        return email

class LoginForm(forms.Form):
    username = forms.EmailField(label="",widget=forms.TextInput(attrs={"placeholder": "E-mail", "class": "input-field", "id": "username"}))
    password = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Пароль", "class": "input-field", "type": "password", "id": "password"}), label="")

    def clean_password(self):
        password = self.cleaned_data["password"]
        username = self.cleaned_data["username"]
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("Неверный email или пароль")
        else:
            if not(check_password(password, user.password)):
                raise ValidationError("Неверный email или пароль")