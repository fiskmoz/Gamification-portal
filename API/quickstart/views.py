from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from quickstart.auth import validate
from quickstart.models import Quiz, QuizEntry
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
from .serializer import FileSerializer
from .models import File


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
        counter = 3 
        name = request.POST.get("Quizname");
        desc = request.POST.get("Description");
        size = request.POST.get("Size");
        quiz = Quiz(QuizName=name, QuizCreator="default", Date = timezone.now()) 
        quiz.save()
        print("Creating a QUIZ!")
        while counter < request.POST - 3:
            
            
        for var in request.POST:
            print(counter)
            if counter == 0:
                name = request.POST.get(var);
            if counter == 1: 
                desc = var;
            if counter == 2:
                size = request.POST.get(var);

                
            if  counter > 2:
                myList.append(request.POST.get(var))
            if counter >= 7:
                quizentry = QuizEntry(QuizID = quiz, Question = myList[0], AlternativeA = myList[1], AlternativeB = myList[2], AlternativeC = myList[3], Correct = myList[4])
                myList.clear()
                counter = 3
                print("Creating a quizentry!")
                quizentry.save()

            counter = counter+1
        return Response(data="SUCCESS! :D ", status = status.HTTP_200_OK)

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser )
    def post(self, request, *args, **kwargs):
#        if request.user.is_anonymous:
#            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
#        if not validate(request.user.username, request.user.password):
#            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):           
        news = File.objects.all()
        serializer = FileSerializer(news, many = True)
        return Response(serializer.data)

