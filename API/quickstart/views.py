from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from quickstart.auth import validate
from quickstart.models import Quiz, QuizEntry, Article
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django.core.files.storage import FileSystemStorage
from .serializer import FileSerializer, QuizSerializer, QuizEntrySerializer, NewsSerializer
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

        name = request.POST.get("Quizname")
        desc = request.POST.get("Description")
        if name == "":
            return
        quiz = Quiz(QuizName=name, QuizCreator="Default") 
        quiz.save() 
        myList = []
        length = int(len(request.POST))
        j = 0
        i = 0
        while i < length-2:
            myList.append(request.POST.get(str(i)))
            if j > 3 :
                quizentry = QuizEntry(QuizID = quiz, Question = myList[0], AlternativeA = myList[1], AlternativeB = myList[2], AlternativeC = myList[3], Correct = myList[4])
                print(quizentry)
                myList.clear()
                j = 0;
                quizentry.save()
            i += 1
            j += 1
        return Response(data="SUCCESS! :D ", status = status.HTTP_200_OK)

class NewsView(APIView):
    def post(self, request, format=None):
#        if request.user.is_anonymous:
#            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
#        if not validate(request.user.username, request.user.password):
#            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        quiz = request.POST.get("ArticleQuiz")
        Title = request.POST.get("ArticleTitle")
        Description = request.POST.get("ArticleDescription")
        if Title == "":
            return
        article = Article(title=Title, description=Description, date = timezone.now())
        article.save()
        return Response(data="SUCCESS! :D ", status = status.HTTP_200_OK)

    def get(self, request, format=None):
        # if request.user.is_anonymous: 
        #     return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        # if not validate(request.user.username, request.user.password):
        #     return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        news = Article.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

class FileView(APIView):
    parser_classes=(FormParser, MultiPartParser,)
    def post(self, request):
#        if request.user.is_anonymous:
#            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
#        if not validate(request.user.username, request.user.password):
#            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        file = request.FILES.get('myfile')
        dictionary = {}
        dictionary['name'] = str(file)
        dictionary['file'] = file
        file_serializer = FileSerializer(data=dictionary)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        file_obj = request.FILES['myfile']
        return Response(status=204)
    def get(self, request):           
        news = File.objects.all()
        serializer = FileSerializer(news, many = True)
        return Response(serializer.data)

