from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',views.index,name="incomes"),
    path('add_inc',views.addinc,name="add_inc"),
    path('income_edit/<int:id>',views.income_edit,name="income_edit"),
    path('income_delete/<int:id>',views.income_delete,name="income_delete"),
    path('search_income',csrf_exempt(views.search_income),name="search_income"),
]