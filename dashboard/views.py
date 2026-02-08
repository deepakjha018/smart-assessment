from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')


@login_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html')