import requests
from django.template import loader, Context
from django.http import HttpResponse
APIaddr = 'http://127.0.0.1:7000/'

def login(request): 
    if request.method == "POST": 
        r = requests.get(APIaddr + 'auth/', )
    if request.method == "GET": 
        template = loader.get_template('login.html')
        context = {}
        return HttpResponse(template.render(context,request))

def homepage(request):
    if request.method == "POST":
        r = requests.get(APIaddr + 'home/', )
    if request.method == "GET":
        template = loader.get_template('home.html')
        context = {}
        return HttpResponse(template.render(context, request))
