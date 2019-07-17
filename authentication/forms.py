from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Userprofile
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe


class CustomUserCreationForm(forms.ModelForm):
    # first_name = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    # last_name = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'email'}))

    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'create a password'}))

    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 're-enter the password'}))

    print(username, email, password)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password2(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        print('these are passwords')
        print(password, password2)

        if password != password2:
            raise forms.ValidationError(
                "passwords does not match"
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    # def clean_username(self):
    #     username = self.cleaned_data['username'].lower()
    #     r = User.objects.filter(username=username)
    #     if r.count():
    #         raise ValidationError("Username already exists")
    #     return username
    #
    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     r = User.objects.filter(email=email)
    #     if r.count():
    #         raise ValidationError("Email already exists")
    #     return email
    #
    # def clean_phonenumber(self):
    #     phonenumber = self.cleaned_data['phonenumber']
    #     r = Userprofile.objects.filter(phone=phonenumber)
    #     if r.count():
    #         raise ValidationError("phone number already exists")
    #     return phonenumber
    #
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("Password don't match")
    #
    #     return password2
    #
    # def save(self):
    #     user = User.objects.create_user(
    #         self.cleaned_data['username'],
    #         self.cleaned_data['email'],
    #         self.cleaned_data['password1'],
    #         first_name = self.cleaned_data['first_name'],
    #         last_name = self.cleaned_data['last_name'],
    #
    #     )
    #
    #     user.save()
    #     return  user


# class HorizontalRadioRenderer(forms.RadioSelect.renderer):
#   def render(self):
#     return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),

]


class Createprofileform(forms.ModelForm):
    phone_number = forms.CharField(label='', max_length=10,
                                   widget=forms.TextInput(attrs={'placeholder': 'phone number'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    # profile_pic = forms.ImageField(label='')
    # gender = forms.ChoiceField(choices=( ('M' , 'Male'),('F' , 'Female') ),
    #                              initial=0,
    #                              widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),
    #                              )
    class Meta:
        model = Userprofile
        fields = ('phone_number', 'profile_pic', 'gender')

    # pro
    #
    #
    # def save(self):
    #     user = Userprofile.objects.create(
    #         phone_number=self.cleaned_data['phone_number'],
    #         profile_pic=self.cleaned_data['profile_pic'],
    #
    #
    #     )
    #
    #     user.save()
    #     return user


class LoginForm(forms.Form):
    username_login = forms.CharField(label='', min_length=4, max_length=150,
                                     widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password_login = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'create a password'}))

    def clean(self):
        username = self.cleaned_data['username_login']
        password = self.cleaned_data['password_login']
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)

        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data['username_login']
        password = self.cleaned_data['password_login']
        user = authenticate(username=username, password=password)
        return user


class UserupdateForm(forms.ModelForm):
    # email = forms.EmailField()
    username = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'email'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileupdateForm(forms.ModelForm):
    phone_number = forms.CharField(label='', max_length=10,
                                   widget=forms.TextInput(attrs={'placeholder': 'phone number'}))
    gender = forms.ChoiceField(choices=(('M', 'Male'), ('F', 'Female')), )

    class Meta:
        model = Userprofile
        fields = ['phone_number', 'profile_pic', 'gender']

