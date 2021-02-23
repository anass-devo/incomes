from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'exp/index.html')

def addexp(request):
    return render(request,'exp/add_exp.html')
