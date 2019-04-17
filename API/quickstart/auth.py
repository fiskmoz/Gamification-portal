from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib import auth
from django.contrib.sessions.models import Session
from django.utils import timezone

class Auth(APIView): 
    def post(self, request, format=None): 
        response = LoginValidate(request.user.username, request.user.password)
        if response is True :
            auth.login(request, request.user)
            return Response(data=request.session.session_key, status=status.HTTP_200_OK)
        else :
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None ): 
        response = LoginValidate(request.user.username, request.user.password)
        if response is True :
            auth.login(request, request.user)
            return Response(data=request.session.session_key, status=status.HTTP_200_OK)
        else :
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)


def LoginValidate(username, password):
    try:
        user = User.objects.get(username=username)
    except user.DoesNotExist:
        return False
    if not user.password == password:
        return False
    return True

def validate(request):
    key = None
    if(request.method == "POST"):
        key = request.POST.get('APISession')
    if(request.method == "GET"):
        key = request.GET.get('APISession')
    try:
        session = Session.objects.get(session_key = key)
        if session is None:
            return False
        return True
    except:
        return False