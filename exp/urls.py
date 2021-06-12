from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',views.index,name="expenses"),
    path('add_exp',views.addexp,name="add_exp"),
    path('expense-edit/<int:id>',views.expense_edit,name="expense-edit"),
    path('expense-delete/<int:id>',views.expense_delete,name="expense-delete"),
    path('search_expenses',csrf_exempt(views.search_expenses),name="search_expenses"),
    path('expense_category_summary',csrf_exempt(views.expense_category_summary),name="expense_category_summary"),
    path('stats',csrf_exempt(views.stats_view),name="stats"),
    path('export_csv',csrf_exempt(views.exportcsv),name="export-csv"),
    path('export_excel',csrf_exempt(views.exportexcel),name="export-excel"),
    path('export_pdf',csrf_exempt(views.exportpdf),name="export-pdf"),
]