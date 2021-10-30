from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from account.forms import CreateUserForm, LogInForm
from django.contrib.auth import login, authenticate, logout


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


def management(request):
    return render(request, 'management.html')
