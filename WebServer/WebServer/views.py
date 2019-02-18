from django.contrib.auth.models import User
from django.contrib import auth
from django.template import loader, Context
from django.http import HttpResponse
import requests
import json

APIUrl = 'http://127.0.0.1:7000/API/' 
def homepage_view(request):
    if not request.user.is_authenticated: 
        return display404(request)
    if request.method == "GET":
        template = loader.get_template('index.html')
        context = {}
        return HttpResponse(template.render(context, request))

def display404(request):
    template = loader.get_template('404.html')
    context = {}
    return HttpResponse(template.render(context,request))

def weeklymission_view(request):
    if not request.user.is_authenticated: 
        return display404(request)
    if request.method == "GET": 
        template = loader.get_template('CreateWeekly.html')
        context = {}
        return HttpResponse(template.render(context, request))

def news_view(request):
    if not request.user.is_authenticated:
        return display404(request)
    if request.method == "GET":
        template = loader.get_template('News.html')
        context = {'User' : request.user}
        return HttpResponse(template.render(context, request))

def getNews_view(request):
    if not request.user.is_authenticated:
        return display404
    if request.method == "GET":
        template = loader.get_template('News.html')
        try:
            context = {
                'News': requests.get(url=APIUrl + 'news/')
            }
            return HttpResponse(template.render(context, request))
        except json.decoder.JSONDecodeError:
            return HttpResponse("JsonDecodeError")