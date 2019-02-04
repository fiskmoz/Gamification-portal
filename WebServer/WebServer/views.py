from django.contrib.auth.models import User
from django.contrib import auth
from django.template import loader, Context
from django.http import HttpResponse

def homepage_view(request):
    if request.method == "GET":
        if not request.user.is_authenticated: 
            return display404(request)
        template = loader.get_template('index.html')
        context = {}
        return HttpResponse(template.render(context, request))

def display404(request):
    template = loader.get_template('404.html')
    context = {}
    return HttpResponse(template.render(context,request))