from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages

import pdb

# Create your views here.

def index(request):
    currency_data=[]
    file_path=os.path.join(settings.BASE_DIR,'currencies.json')

    with open(file_path,'r') as json_file:
        data = json.load(json_file)

        for k,v in data.items():
            currency_data.append({"name":k,"value":v})

        #pdb.set_trace() # ddebbogger qui bloque le process pour tester qlq chose

    exists = UserPreference.objects.filter(user=request.user).exists()
    User_preferences = None
    
    if exists:
        User_preferences = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request,'preferences/index.html',{"currencies":currency_data,"User_preferences":User_preferences})
    else:
        currency=request.POST['currency']
        if exists:
            User_preferences.currency = currency
            User_preferences.save()
        else:
            UserPreference.objects.create(user=request.user,currency=currency)
        messages.success(request,'Changes saved !')
        return render(request,'preferences/index.html',{"currencies":currency_data,"User_preferences":User_preferences})





