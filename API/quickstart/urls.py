"""API URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from . import auth
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('' ,views.Home.as_view()),
    path('auth/', auth.Auth.as_view()),
    path('quiz/', views.GetAllOrAppendQuiz.as_view()),
    path('quiz/article/<id>/', views.GetQuizByArticleId.as_view()),
    path('article/', views.GetAllOrAppendArticle.as_view()), 
    path('article/<id>/', views.GetArticleById.as_view()),
    path('article/<id>/score/', views.GetAndSetScoreForArticle.as_view()),
    path('fileupload/', views.FileUpload.as_view()),
    path('highscores/', views.GetAllHighScores.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)