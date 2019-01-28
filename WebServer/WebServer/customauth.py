import requests
from django.template import loader, Context
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth import logout
APIaddr = 'http://127.0.0.1:7000/'

def login_view(request): 
    if request.method == "POST": 
        username = request.POST.get('username')
        password = request.POST.get('password')
        r = requests.post(APIaddr + 'auth/', auth=(username, password))
        if r.ok: 
            user = None
            try:
                user = User.objects.get(username=username)
            except :
                user = User.objects.create_user(username=username, email='', password=password)
            user = auth.authenticate(username=username, password=password)
            if user is None or not user.is_active:
                return redirect('login')
            auth.login(request, user)
            return redirect('home')

    if request.method == "GET": 
        template = loader.get_template('login.html')
        context = {}
        return HttpResponse(template.render(context,request))

def logout_view(request):
    logout(request)
    return redirect('login')

