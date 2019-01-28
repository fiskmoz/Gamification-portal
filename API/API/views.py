from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from API.auth import validate
from rest_framework import status

class Home(APIView): 
    def get(self, request, format=None): 
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

class Auth(APIView): 
    def post(self, request, format=None): 
        response = validate(request.user.username, request.user.password)
        if response is True :
            return Response(data='You are authenticated!', status=status.HTTP_200_OK)
        else :
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)