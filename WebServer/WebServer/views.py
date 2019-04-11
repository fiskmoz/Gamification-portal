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
        return HttpResponse(template.render(context, request))

def create_view_quiz(request):
    if not request.user.is_authenticated: 
        return display404(request)
    if request.method == "GET": 
        template = loader.get_template('Create/quiz.html')
        context = {'me' : request.user.username}
        return HttpResponse(template.render(context, request))

def create_view_article(request):
    if not request.user.is_authenticated: 
        return display404(request)
    if request.method == "GET": 
        template = loader.get_template('Create/article.html')
        context = {'me' : request.user.username}
        return HttpResponse(template.render(context, request))

def news_view(request):
    if not request.user.is_authenticated:
        return display404(request)
    if request.method == "GET":
        template = loader.get_template('News/news.html')
        context = {'me' : request.user}
        return HttpResponse(template.render(context, request))

def article_view(request,id):
    if not request.user.is_authenticated:
        return display404(request)
    if request.method == "GET":
        template = loader.get_template('News/article.html')
        context = {'me' : request.user, 'ID' : id}
        return HttpResponse(template.render(context, request))

def articleQuiz_view(request,id):
    if not request.user.is_authenticated:
        return display404(request)
    if request.method == "GET":
        template = loader.get_template('News/articleQuiz.html')
        context = {'me': request.user, 'ID' : id}
        return HttpResponse(template.render(context, request))

def getNews_view(request):
    if not request.user.is_authenticated:
        return display404
    if request.method == "GET":
        template = loader.get_template('News.html')
        try:
            context = {
                'News': requests.post(url=APIUrl + 'news/', data=({'filename': request.filename}))
            }
            return HttpResponse(template.render(context, request))
        except json.decoder.JSONDecodeError:
            return HttpResponse("JsonDecodeError")

def highscores_view(request):
    if not request.user.is_authenticated:
        return display404
    if request.method == "GET":
        template = loader.get_template('highscores.html')
        context = {'me': request.user, 'ID' : id}
        return HttpResponse(template.render(context, request))