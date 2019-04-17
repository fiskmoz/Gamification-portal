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

def create_view(request):
    if not request.user.is_authenticated: 
        return display404(request)
    if request.method == "GET": 
        template = loader.get_template('Create/create.html')
        context = {}
        return HttpResponse(template.render(getContext(request, id ), request))

def create_view_quiz(request):
    if not request.user.is_authenticated: 
        return display404(request)
    if request.method == "GET": 
        template = loader.get_template('Create/quiz.html')
        return HttpResponse(template.render(getContext(request, id ), request))

def create_view_article(request):
    if not request.user.is_authenticated: 
        return display404(request)
    if request.method == "GET": 
        template = loader.get_template('Create/article.html')
        return HttpResponse(template.render(getContext(request, id ), request))

def news_view(request):
    if not request.user.is_authenticated:
        return display404(request)
    if request.method == "GET":
        template = loader.get_template('News/news.html')
        return HttpResponse(template.render(getContext(request, id ), request))

def article_view(request,id):
    if not request.user.is_authenticated:
        return display404(request)
    if request.method == "GET":
        template = loader.get_template('News/article.html')
        return HttpResponse(template.render(getContext(request, id ), request))

def articleQuiz_view(request,id):
    if not request.user.is_authenticated:
        return display404(request)
    if request.method == "GET":
        template = loader.get_template('News/articleQuiz.html')
        return HttpResponse(template.render(getContext(request, id ), request))

def getNews_view(request):
    if not request.user.is_authenticated:
        return display404
    if request.method == "GET":
        template = loader.get_template('News.html')
        return HttpResponse(template.render(getContext(request, id ), request))

def highscores_view(request):
    if not request.user.is_authenticated:
        return display404
    if request.method == "GET":
        template = loader.get_template('highscores.html')
        return HttpResponse(template.render(getContext(request, id ), request))


def getContext(request, id):
    return {'me' : request.user, 'ID': id, 'APISession' : request.session['APISession']}