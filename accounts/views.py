from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'accounts/main.html')


def login(request):
    return render(request, 'accounts/login.html')
