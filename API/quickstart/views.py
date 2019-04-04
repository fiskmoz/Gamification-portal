from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from quickstart.auth import validate
from quickstart.models import Quiz, QuizEntry, Article, ArticleLink, QuizLink, ArticleScore
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django.core.files.storage import FileSystemStorage
from .serializer import FileSerializer, QuizSerializer, QuizEntrySerializer, NewsSerializer, ArticleScoreSerializer
from .models import File
import json
import operator


class Home(APIView): 
    def get(self, request, format=None): 
        if request.user.is_anonymous:
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        if not validate(request.user.username, request.user.password):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

class SpecificQuizView(APIView):
    lookup_field = 'name'
    def get(self, requst, format=None):
        quiz = Quiz.objects.get(name = name)
        serializer = QuizSerializer(quiz, many=False)
        return Response(serializer.data)

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
        # print(request.POST)

        name = request.POST.get("Quizname")
        desc = request.POST.get("Description")
        if name == "":
            return
        quiz = Quiz(name=name, description = desc , creator = request.user.username) 
        quiz.save() 
        myList = []
        length = int(len(request.POST))
        # print(length)
        j = 0
        i = 0
        while i < length-2:
            myList.append(request.POST.get(str(i)))
            # print(i)
            if j > 3 :
                # print(myList)
                quizentry = QuizEntry(quiz = quiz, question = myList[0], alta = myList[1], altb = myList[2], altc = myList[3], correct = myList[4])
                # print(quizentry)
                myList.clear()
                j = 0
                i += 1
                quizentry.save()
                continue
            i += 1
            j += 1
        return Response(data="SUCCESS! :D ", status = status.HTTP_200_OK)

class NewsView(APIView):
    def post(self, request, format=None):
#        if request.user.is_anonymous:
#            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
#        if not validate(request.user.username, request.user.password):
#            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        # print(request.POST)
        quizID = request.POST.get("ArticleQuiz")
        Title = request.POST.get("ArticleTitle")
        Description = request.POST.get("ArticleDescription")
        ShortDesc = request.POST.get("ArticleShortDescription")
        # print(quizID)
        # print(Title)
        # print(Description)
        if Title == "":
            return
        article = Article(title=Title, description=Description, subtitle = ShortDesc, date = timezone.now())
        article.save()
        #TODO:Fixa "unika" namn
        if quizID != "":
            quiz = Quiz.objects.get(id=quizID)
            articleID = Article.objects.get(title = Title)
            quizLink = QuizLink(article=articleID, quiz=quiz)
            quizLink.save()
        return Response(data=article.id, status = status.HTTP_200_OK)

    def get(self, request, format=None):
        # if request.user.is_anonymous: 
        #     return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        # if not validate(request.user.username, request.user.password):
        #     return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        news = Article.objects.all().order_by("-date")
        serializer = NewsSerializer(news, many=True)
        # print(serializer.data)
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

    def put(self,request):
        artID = request.POST.get("ArticleID")
        FileID = request.POST.get("FileID")
        article_link = ArticleLink(article=Article.objects.get(id= artID), filepath=File.objects.get(id = FileID))
        article_link.save()
        return Response("GREAT SUCCEsSS!!sadas", status=status.HTTP_201_CREATED)

class IndividualNewsView(APIView):
    def get(self, request, id):
        article = Article.objects.get(id= id)
        try: 
            linkobj = ArticleLink.objects.get(article = article)
            path = File.objects.get(id = linkobj.filepath.id)
            serializer = NewsSerializer(article, many=False)
            return Response({'article' : serializer.data, 'filepath': path.file.name})
        except :
            serializer = NewsSerializer(article, many=False)
            return Response({'article' : serializer.data, 'filepath': "No File Provided"})

class IndividualNewsViewQuiz(APIView):
    lookup_field = 'id'
    def get(self, request, id):
        quizes = set()
        quizentries = set()
        for item in QuizLink.objects.filter(article= id):
            quizes.add(item.quiz)
            # print(item.quiz.id)
            for nrquiz in QuizEntry.objects.filter(quiz= item.quiz):
                quizentries.add(nrquiz)
        serializer = QuizSerializer(quizes, many=True)
        serializer2 = QuizEntrySerializer(quizentries, many=True)
        return Response({
            'quiz': serializer.data,
            'quizentry': serializer2.data
            })

class IndividualNewsViewFiles(APIView):
    def get(self, request, id):
        files = set()
        for fileLink in ArticleLink.objects.filter(article= id):
            files.add(fileLink.filePath)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

class ArticleScoreView(APIView):

    def get(self, request):
        pass

    def post(self, request,*args, **kwargs):
        articleID = request.POST.get('articleID') # DEHÄR ÄR QUIZ ID 
        # print(request.POST)
        score=0
        i=0
        quizanswers = []
        length = int(len(request.POST))
        while i< length-2:
            quizanswers.append(request.POST.get(str(i)))
            # print(quizanswers[i])
            i += 1
        correctquizanswers = []
        item = QuizLink.objects.get(article = Article.objects.get(id = articleID))
        # print(item.quiz)
        for nrquiz in QuizEntry.objects.filter(quiz= item.quiz):
            correctquizanswers.append(nrquiz.correct)
        i=0
        for answere in quizanswers:
            if correctquizanswers[i]== answere:
                score+=1
            i+=1
        articlescore = ArticleScore(username=request.user.username, article=item.article, score=score)
        articlescore.save()
        return Response("GREAT SUCCEsSS!!sadas", status=status.HTTP_201_CREATED)


