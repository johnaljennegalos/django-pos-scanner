from django.contrib.admin.templatetags.admin_list import items_for_result
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .models import Product, Employee, Branch, BranchInventory


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

@login_required(login_url='login')
def branchInventory(request):
    try:
        login_employee = Employee.objects.get(user=request.user)
        assigned_branch = login_employee.branch

        items = BranchInventory.objects.filter(branch=assigned_branch).select_related('product', 'product__supplier')


    except Employee.DoesNotExist:
        items = BranchInventory.objects.none()

    return render(request, 'accounts/branch_inventory.html', {'items':items})
