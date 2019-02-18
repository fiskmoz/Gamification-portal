from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from quickstart.auth import validate
from quickstart.models import Quiz, QuizEntry
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
from .serializer import FileSerializer


class Home(APIView): 
    def get(self, request, format=None): 
        if request.user.is_anonymous:
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        if not validate(request.user.username, request.user.password):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

class QuizView(APIView): 
    def post(self, request, format=None): 
        # if request.user.is_anonymous: 
        #     return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        # if not validate(request.user.username, request.user.password):
        #     return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        # quiz = Quiz()
        print(request.POST)
        print(request)
        return Response(data="SUCCESS! :D ", status = status.HTTP_200_OK)

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser )
    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        if not validate(request.user.username, request.user.password):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


