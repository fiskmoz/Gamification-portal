from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib import auth
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import Permission

class Auth(APIView): 
    def post(self, request, format=None): 
        return LoginValidation(request)

    def get(self, request, format=None ): 
        return LoginValidation(request)
        

def LoginValidation(request):
    user = None
    try:
        user = User.objects.get(username=request.user.username)
    except user.DoesNotExist:
        return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
    if not user.password == request.user.password:
        return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
    auth.login(request, request.user)
    role = "user"
    if request.user.is_superuser:
        role = "superuser"
    return Response(data={'APISession' : request.session.session_key, 'Role' : role}, status=status.HTTP_200_OK)

def validate(request):
    key = getKey(request)
    try:
        session = Session.objects.get(session_key = key)
        if session is None:
            return False
        return True
    except:
        return False

def checkPriveledge(request):
    key = getKey(request)
    session = Session.objects.get(session_key = key)
    session_data = session.get_decoded()
    user = User.objects.get(id=session_data.get('_auth_user_id'))
    if user.is_superuser:
        return True
    return False

def getKey(request):
    key = None
    if(request.method == "POST"):
        key = request.POST.get('APISession')
    if(request.method == "GET"):
        key = request.GET.get('APISession')
    if(request.method == "PATCH"):
        key = request.POST.get('APISession')
    return key
