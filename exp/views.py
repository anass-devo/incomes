from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Expense,Category
from userpreferences.models import UserPreference
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime,timedelta
import json
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum
import csv
import xlwt

# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('SearchText')
        expenses = Expense.objects.filter(amount__istartswith=search_str ,owner=request.user) | Expense.objects.filter(
                   date__istartswith=search_str ,owner=request.user) | Expense.objects.filter(
                   description__icontains=search_str ,owner=request.user) | Expense.objects.filter(
                   category__icontains=search_str ,owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data),safe=False)

@login_required(login_url = "/authentication/login")
def index(request):
    Categories=Category.objects.all()
    expenses=Expense.objects.filter(owner=request.user)
    paginator=Paginator(expenses,4)
    page_number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    currency=UserPreference.objects.get(user=request.user).currency
    context={
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency,
        }
    return render(request,'exp/index.html',context)

@login_required(login_url = "/authentication/login")
def addexp(request):
    Categories=Category.objects.all()
    context={
        'Categories':Categories,
        'values':request.POST
        }
    if request.method == "GET":
      return render(request,'exp/add_exp.html',context)
    if request.method == "POST":
        amount=request.POST["amount"]
        category=request.POST["category"]
        description=request.POST["description"]
        date=request.POST["date"]
        if not amount:
            messages.error(request,"Amount field is required !! Please fill all the informations")
            return render(request,'exp/add_exp.html',context)
        if not description:
            messages.error(request,"Description is required !! Please fill all the informations")
            return render(request,'exp/add_exp.html',context)
  
        Expense.objects.create(owner=request.user,amount=amount,description=description,category=category,date=date)
        messages.success(request,"Expense saved Successfully !")
        return redirect("expenses")

@login_required(login_url = "/authentication/login")
def expense_edit(request,id):
    expense=Expense.objects.get(pk=id)
    Categories=Category.objects.all()
    context={
        'expense':expense,
        'values':expense,
        'Categories':Categories,
    }

    if request.method =='GET':
        return render(request,'exp/expense-edit.html',context)
    if request.method == "POST":
        amount=request.POST["amount"]
        category=request.POST["category"]
        description=request.POST["description"]
        date=request.POST["date"]
        if not amount:
            messages.error(request,"Amount field is required !! Please fill all the informations")
            return render(request,'exp/expense-edit.html',context)
        if not description:
            messages.error(request,"Description is required !! Please fill all the informations")
            return render(request,'exp/expense-edit.html',context)
        expense.owner=request.user
        expense.amount=amount
        expense.description=description
        expense.category=category
        expense.date=date
        expense.save()
        messages.success(request,"Expense Updated Successfully !")
        return redirect("expenses")

@login_required(login_url = "/authentication/login")
def expense_delete(request,id):
    expense=Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,"Expense Removed Successfully !")
    return redirect("expenses")

def expense_category_summary(request):
    todays_date=datetime.today()
    six_months_ago=todays_date-timedelta(days=30*6)
    expenses=Expense.objects.filter(owner=request.user,date__gte=six_months_ago,date__lte=todays_date)
    finalrep={}

    def get_category(expense):
        return expense.category

    category_list=list(set(map(get_category,expenses)))

    def get_expense_category_amount(category):
        amount=0
        filtred_by_category=expenses.filter(category=category)

        for item in filtred_by_category:
            amount +=item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)
    return JsonResponse({"expense_category_data":finalrep},safe=False)

def stats_view(request):
    return render(request,'exp/stats.html')

def exportcsv(request):
    response= HttpResponse(content_type='text/csv')
    response["Content-Disposition"]= 'attachement; filename=Expenses' + str(datetime.now()) +'.csv'
    writer= csv.writer(response)
    writer.writerow(["Amount","Description","Category","Date"])

    expenses=Expense.objects.filter(owner=request.user)
    
    for exp in expenses:
        writer.writerow([exp.amount,exp.description,exp.category,exp.date])

    return response

def exportexcel(request):
    response= HttpResponse(content_type='application/ms-excel')
    response["Content-Disposition"]= 'attachement; filename=Expenses' + str(datetime.now()) +'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Expenses")
    row_num=0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["Amount","Description","Category","Date"]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style=xlwt.XFStyle()
    rows=Expense.objects.filter(owner=request.user).values_list("amount","description","category","date")

    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response

def exportpdf(request):
    response= HttpResponse(content_type='application/pdf')
    response["Content-Disposition"]= 'inline; attachement; filename=Expenses' + str(datetime.now()) +'.pdf'
    response["Content-Transfer-Encoding"]='binary'

    expenses=Expense.objects.filter(owner=request.user)
    sum=expenses.aggregate(Sum('amount'))

    html_string = render_to_string("exp/pdf_output.html",{"expenses":expenses,"total":sum["amount__sum"]})
    html=HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response
