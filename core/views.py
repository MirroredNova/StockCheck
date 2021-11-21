from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import Product, UserProduct

# Create your views here.


def home_page(request):
    return render(request, 'home_page.html')


@login_required(login_url='/login/')
def dashboard(request):
    product = UserProduct.objects.filter(username=request.user)
    # userprods = []
    # for pr in product:
    #     print(pr.product_name.product_name)
    return render(request, 'dashboard.html', {'UserProduct': product})
