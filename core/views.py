from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


def home_page(request):
    return render(request, 'home_page.html')


@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')
