from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class Auth(APIView): 
    def post(self, request, format=None): 
        response = validate(request.user.username, request.user.password)
        if response is True :
            return Response(data='You are authenticated!', status=status.HTTP_200_OK)
        else :
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None ): 
        response = validate(request.user.username, request.user.password)
        if response is True :
            return Response(data='You are authenticated!', status=status.HTTP_200_OK)
        else :
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)


def validate(username, password):
    try:
        user = User.objects.get(username=username)
    except user.DoesNotExist:
        return False
    if not user.password == password:
        return False
    return True
