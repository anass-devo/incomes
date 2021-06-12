from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Income,Source
from userpreferences.models import UserPreference
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

# Create your views here.

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('SearchText')
        incomes = Income.objects.filter(amount__istartswith=search_str ,owner=request.user) | Income.objects.filter(
                   date__istartswith=search_str ,owner=request.user) | Income.objects.filter(
                   description__icontains=search_str ,owner=request.user) | Income.objects.filter(
                   source__icontains=search_str ,owner=request.user)
        data = incomes.values()
        return JsonResponse(list(data),safe=False)

@login_required(login_url = "/authentication/login")
def index(request):
    Sources=Source.objects.all()
    incomes=Income.objects.filter(owner=request.user)
    paginator=Paginator(incomes,4)
    page_number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    currency=UserPreference.objects.get(user=request.user).currency
    context={
        'incomes':incomes,
        'page_obj':page_obj,
        'currency':currency,
        }
    return render(request,'income/index.html',context)

@login_required(login_url = "/authentication/login")
def addinc(request):
    Sources=Source.objects.all()
    context={
        'Sources':Sources,
        'values':request.POST
        }
    if request.method == "GET":
      return render(request,'income/add_inc.html',context)
    if request.method == "POST":
        amount=request.POST["amount"]
        source=request.POST["source"]
        description=request.POST["description"]
        date=request.POST["date"]
        if not amount:
            messages.error(request,"Amount field is required !! Please fill all the informations")
            return render(request,'income/add_inc.html',context)
        if not description:
            messages.error(request,"Description is required !! Please fill all the informations")
            return render(request,'income/add_inc.html',context)
  
        Income.objects.create(owner=request.user,amount=amount,description=description,source=source,date=date)
        messages.success(request,"Income saved Successfully !")
        return redirect("incomes")

@login_required(login_url = "/authentication/login")
def income_edit(request,id):
    income=Income.objects.get(pk=id)
    Sources=Source.objects.all()
    context={
        'income':income,
        'values':income,
        'Sources':Sources,
    }

    if request.method =='GET':
        return render(request,'income/income_edit.html',context)
    if request.method == "POST":
        amount=request.POST["amount"]
        source=request.POST["source"]
        description=request.POST["description"]
        date=request.POST["date"]
        if not amount:
            messages.error(request,"Amount field is required !! Please fill all the informations")
            return render(request,'income/income_edit.html',context)
        if not description:
            messages.error(request,"Description is required !! Please fill all the informations")
            return render(request,'income/income_edit.html',context)
        income.owner=request.user
        income.amount=amount
        income.description=description
        income.source=source
        income.date=date
        income.save()
        messages.success(request,"income Updated Successfully !")
        return redirect("incomes")

@login_required(login_url = "/authentication/login")
def income_delete(request,id):
    income=Income.objects.get(pk=id)
    income.delete()
    messages.success(request,"Income Removed Successfully !")
    return redirect("incomes")
