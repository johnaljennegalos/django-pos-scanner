from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .models import Product


# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/main.html')

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
            # else:
            # messages.info(request, 'Username or password is incorrect.')

    # context = {}
    return render(request, 'accounts/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')



def productsPage(request):
    ps = Product.objects.all()

    context = {'ps': ps}

    return render(request, 'accounts/products.html', context)
