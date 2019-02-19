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
        print(request.POST)
        counter = 3 
        name = request.POST.get("Quizname")
        desc = request.POST.get("Description")
        size = request.POST.get("Size")
        if name == "":
            return
        quiz = Quiz(QuizName=name, QuizCreator="default", Date = timezone.now()) 
        quiz.save()
        print("Creating a QUIZ!")
        myList = []
        length = int(len(request.POST))
        while counter < length:
            myList.append(request.POST.get(str(counter)))
            tempLen = int(len(myList))
            print("Counter: " + str(counter) + "Appended: " + request.POST.get(str(counter)) + "TempLen: " + str(tempLen) + "lenght: " + str(length))
            if tempLen > 4 :
                quizentry = QuizEntry(QuizID = quiz, Question = myList[0], AlternativeA = myList[1], AlternativeB = myList[2], AlternativeC = myList[3], Correct = myList[4])
                myList.clear()
                print("Creating QuizEntry")
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

