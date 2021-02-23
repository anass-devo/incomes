from django.urls import path
from . import views



urlpatterns = [
    path('',views.index,name="expenses"),
    path('add_exp',views.addexp,name="add_exp")
]