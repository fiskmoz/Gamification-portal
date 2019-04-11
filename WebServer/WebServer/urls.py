"""WebServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import customauth
from . import views

urlpatterns = [
    path('', views.homepage_view, name='home'),
    path('login/', customauth.login_view, name='login'),
    path('logout/', customauth.logout_view, name= 'logout'),
    path('news/', views.news_view, name='news'),
    path('news/<id>', views.article_view, name='specific_article'),
    path('news/quiz/<id>', views.articleQuiz_view, name='articleQuiz'),
    path('create/', views.create_view, name="create"),
    path('create/quiz/', views.create_view_quiz, name="create_quiz"),
    path('create/article/', views.create_view_article, name="create_article"),
    path('highscores/', views.highscores_view, name="highscores"),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)