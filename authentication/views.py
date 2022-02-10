from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from authentication import forms
from authentication.models import User


def homepage(request):
    if request.user.is_authenticated:
        return redirect('flow')

    username_form = forms.UsernameForm()
    password_form = forms.PasswordForm()

    if request.method == 'POST':

        username_form = forms.UsernameForm(request.POST)
        password_form = forms.PasswordForm(request.POST)

        if username_form.is_valid() and password_form.is_valid():

            user = authenticate(
                username=username_form.cleaned_data['username'],
                password=password_form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                return redirect('flow')
            else:
                message = 'Identifiants invalides.'

    return render(request, 'authentication/homepage.html', locals())


def signup_page(request):
    username_form = forms.UsernameForm()
    password_form = forms.PasswordForm()
    repeat_pwd_form = forms.PasswordForm()

    if request.method == 'POST':

        username_form = forms.UsernameForm(request.POST)
        password_form = forms.PasswordForm(request.POST)
        repeat_pwd_form = forms.PasswordForm(request.POST)

        if username_form.is_valid() and password_form.is_valid() and repeat_pwd_form.is_valid():

            user = User.objects.create_user(username=username_form.cleaned_data['username'],
                                            password=password_form.cleaned_data['password'])
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'authentication/signup.html', locals())


def logout_view(request):
    logout(request)
    return redirect('home')
