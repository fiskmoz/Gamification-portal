from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from quickstart.auth import validate
from quickstart.models import Quiz, QuizEntry
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django.core.files.storage import FileSystemStorage
from .serializer import FileSerializer, QuizSerializer, QuizEntrySerializer
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
    def get(self, request, format=None): 
        # if request.user.is_anonymous: 
        #     return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        # if not validate(request.user.username, request.user.password):
        #     return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        quizes = Quiz.objects.all()
        serializer = QuizSerializer(quizes, many = True)
        return Response(serializer.data)

    def post(self, request, format=None): 
        # if request.user.is_anonymous: 
        #     return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        # if not validate(request.user.username, request.user.password):
        #     return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        print(request.POST)
        counter = 3 
        name = request.POST.get("Quizname")
        desc = request.POST.get("Description")
        size = request.POST.get("Size")
        if name == "":
            return
        quiz = Quiz(QuizName=name, QuizCreator="default", Date = timezone.now()) 
        quiz.save()
        myList = []
        length = int(len(request.POST))
        while counter < length:
            myList.append(request.POST.get(str(counter)))
            tempLen = int(len(myList))
            if tempLen > 4 :
                quizentry = QuizEntry(QuizID = quiz, Question = myList[0], AlternativeA = myList[1], AlternativeB = myList[2], AlternativeC = myList[3], Correct = myList[4])
                myList.clear()
                quizentry.save()
            counter = counter+1
        return Response(data="SUCCESS! :D ", status = status.HTTP_200_OK)

class FileView(APIView):
    parser_classes=(FormParser, MultiPartParser,)
    def post(self, request):
#        if request.user.is_anonymous:
#            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
#        if not validate(request.user.username, request.user.password):
#            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        # file_serializer = FileSerializer(data=request.data)
        file = request.FILES.get('myfile')
        print(file)
        # if 'file' not in request.data:
        #     raise ParseError("Empty Content")
        # r = request.data['myfile']
        # print(request.FILES)
        # file_obj = request.FILES['myfile']
        return Response(status=204)
        # else:
        #     return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        file_obj = request.FILES['myfile']
        return Response(status=204)
    def get(self, request):           
        news = File.objects.all()
        serializer = FileSerializer(news, many = True)
        return Response(serializer.data)

