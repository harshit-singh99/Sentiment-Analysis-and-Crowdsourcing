from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='', min_length=4, max_length=150,widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.EmailField(label='',widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'create a password'}))
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 're-enter the password'}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        user.save()
        return  user

class LoginForm(forms.Form):
    username_login = forms.CharField(label='', min_length=4, max_length=150,widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password_login = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'create a password'}))


    def clean(self):
        username = self.cleaned_data['username_login']
        password = self.cleaned_data['password_login']
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data['username_login']
        password = self.cleaned_data['password_login']
        user = authenticate(username=username, password=password)
        return user




