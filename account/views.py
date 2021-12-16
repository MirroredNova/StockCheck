from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from account.forms import *


def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/dashboard')
            else:
                messages.info(request, 'That user doesn\'t exist or the password is incorrect.')
    else:
        form = LogInForm()

    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/dashboard')
    else:
        form = CreateUserForm()
    return render(request, 'signup.html', {
        'form': form,
    })


def log_out(request):
    logout(request)
    return redirect("/")


@login_required(login_url='/login/')
def management(request):
    initial_vals = {'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                    'phone': request.user.phone,
                    'discord_webhook_url': request.user.discord_webhook_url}

    if request.method == 'POST':
        form = AccountManagementForm(request.POST, initial=initial_vals)
        if form.is_valid():
            fs = form.save(commit=False)
            u = User.objects.get(username=request.user.username)
            u.first_name = fs.first_name
            u.last_name = fs.last_name
            u.email = fs.email
            u.phone = fs.phone
            u.discord_webhook_url = fs.discord_webhook_url
            u.save()
            messages.info(request, 'Your information has been changed successfully!')
            return redirect('/management/')
    else:
        form = AccountManagementForm(initial=initial_vals)
    return render(request, 'management.html', {
        'form': form,
    })


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/management/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_management/password_change.html', {
        'form': form
    })
