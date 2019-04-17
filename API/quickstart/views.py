from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from quickstart.auth import validate, checkPriveledge
from quickstart.models import Quiz, QuizEntry, Article, ArticleLink, QuizLink, ArticleScore
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django.core.files.storage import FileSystemStorage
from .serializer import FileSerializer, QuizSerializer, QuizEntrySerializer, NewsSerializer, ArticleScoreSerializer
from .models import File
import json
import operator
from django.db.models import Sum
from datetime import timedelta

# Homepage
# http://127.0.0.1:7000/v1/
class Home(APIView): 
    def get(self, request, format=None): 
        if request.user.is_anonymous:
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

#################################################################################
# Quiz part #

# GET: Get all quizes
# POST: Create and parse a quiz
# http://127.0.0.1:7000/v1/quiz/
class GetAllOrAppendQuiz(APIView): 
    def get(self, request, format=None): 
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        quizes = Quiz.objects.all()
        serializer = QuizSerializer(quizes, many = True)
        return Response(serializer.data)

    def post(self, request, format=None): 
        print(request.POST)
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        if not checkPriveledge(request):
            return Response("Not enough priveledge", status=status.HTTP_401_UNAUTHORIZED)
        name = request.POST.get("Quizname")
        desc = request.POST.get("Description")
        creator = request.POST.get("Creator")
        timer = request.POST.get("Quiztimer")
        if not InputCheck(name) or not InputCheck(creator) or not InputCheck(timer):
            print("QUIZ IS NOT FINE")
            return Response("Invalid Input", status=status.HTTP_406_NOT_ACCEPTABLE)
        length = int(len(request.POST))-5
        if (length)%5 != 0: 
            return Response("Invalid Input", status=status.HTTP_406_NOT_ACCEPTABLE)
        i = 0
        while i < length:
            if not InputCheck(request.POST.get(str(i))):
                return Response("Invalid Input", status=status.HTTP_406_NOT_ACCEPTABLE)
            i += 1
        quiz = Quiz(name=name, description = desc , creator = creator, quiztimer = timer) 
        quiz.save() 
        myList = []
        i = 0
        while i < length:
            myList.append(request.POST.get(str(i)))
            i += 1
            if i > 4 and i%5 is 0 :
                quizentry = QuizEntry(quiz = quiz, question = myList[0], alta = myList[1], altb = myList[2], altc = myList[3], correct = myList[4])
                myList.clear()
                quizentry.save()
        return Response(data="Created", status = status.HTTP_200_OK)


# GET: Get an entire quiz by article ID.
# http://127.0.0.1:7000/v1/news/quiz/<id>/
class GetQuizByArticleId(APIView):
    lookup_field = 'id'
    def get(self, request, id):
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
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

# Get a specific quiz
# http://127.0.0.1:7000/v1/ ???? 
# class SpecificQuizView(APIView):
#     lookup_field = 'name'
#     def get(self, requst, format=None):
#         quiz = Quiz.objects.get(name = name)
#         serializer = QuizSerializer(quiz, many=False)
#         return Response(serializer.data)

#################################################################################
# Article Part

# GET: get all artcile objects
# POST: Create a new article
# http://127.0.0.1:7000/v1/article/
class GetAllOrAppendArticle(APIView):

    def get(self, request, format=None):
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        if not validate(request):
            return Response("Auth failed", status = status.HTTP_405_METHOD_NOT_ALLOWED)
        news = Article.objects.all().order_by("-date")
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        if not checkPriveledge(request):
            return Response("Not enough priveledge", status=status.HTTP_401_UNAUTHORIZED)
        #TODO: SAFETYCHECKS.
        quizID = request.POST.get("ArticleQuiz")
        Title = request.POST.get("ArticleTitle")
        Description = request.POST.get("ArticleDescription")
        ShortDesc = request.POST.get("ArticleShortDescription")
        if not InputCheck(Title):
            return Response("Invalid Input", status=status.HTTP_406_NOT_ACCEPTABLE)
        article = Article(title=Title, description=Description, subtitle = ShortDesc, date = timezone.now(), creator= request.POST.get("Creator"))
        article.save()
        #TODO:Fixa "unika" namn
        if quizID != "":
            quiz = Quiz.objects.get(id=quizID)
            articleID = Article.objects.get(title = Title)
            quizLink = QuizLink(article=articleID, quiz=quiz)
            quizLink.save()
        return Response(data=article.id, status = status.HTTP_200_OK)

# GET: Get individual article object by ID.
# http://127.0.0.1:7000/v1/article/<id>/
class GetArticleById(APIView):
    def get(self, request, id):
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        article = Article.objects.get(id= id)
        done = False
        try:
            articleScore = ArticleScore.objects.get(article=article, username= request.GET.get('User') )
            done = articleScore.done;
        except:
            pass
        try: 
            linkobj = ArticleLink.objects.get(article = article)
            path = File.objects.get(id = linkobj.filepath.id)
            serializer = NewsSerializer(article, many=False)
            return Response({'article' : serializer.data, 'filepath': path.file.name, 'done' : done})
        except :
            serializer = NewsSerializer(article, many=False)
            return Response({'article' : serializer.data, 'filepath': None, 'done': done})

# GET: Pass
# POST: Set the initial user score for a specific quiz.
# PATCH: Update the initial user score for a specific quiz.
# http://127.0.0.1:7000/v1/article/<id>/score/
class GetAndSetScoreForArticle(APIView):

    def get(self, request, id):
        pass

    def post(self, request, id,*args, **kwargs):
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        try:
            article = Article.objects.get(id = id)
        except: 
            return Response("Invalid Input", status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            articleScore = ArticleScore.objects.get(article = article, username = request.POST.get('Creator'))
        except:
            articleScore = ArticleScore(username = request.POST.get('Creator'), article=article, score=0, done=False ,date= timezone.now())
        if articleScore.done is True:
            return Response("Already done", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if articleScore.started is False:
            articleScore.started = True
            articleScore.save()
        return Response("Quiz Started", status=status.HTTP_200_OK)

    def patch(self, request, id, *args, **kwargs):
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        if not InputCheck(request.POST.get('Creator')):
            return Response("Invalid Input", status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            article = Article.objects.get(id = id)
        except:
            return Response("Invalid Input", status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            articleScore = ArticleScore.objects.get(article = article, username=request.POST.get('Creator'))
        except:
            return Response("Invalid Input", status=status.HTTP_406_NOT_ACCEPTABLE)
        time = timezone.now() - articleScore.date
        if time > timedelta(seconds= 600):
            articleScore.done = True
            articleScore.save()
        if articleScore.done:
            return Response("Saved", status=status.HTTP_200_OK)
        i=0
        while i < int(len(request.POST))-3:
            if not InputCheck(request.POST.get(str(i))):
                return Response("Invalid Input", status=status.HTTP_406_NOT_ACCEPTABLE)
        quizanswers = []
        while i< int(len(request.POST))-3:
            quizanswers.append(request.POST.get(str(i)))
            i += 1
        correctquizanswers = []
        item = QuizLink.objects.get(article = article)
        for nrquiz in QuizEntry.objects.filter(quiz= item.quiz):
            correctquizanswers.append(nrquiz.correct)
        i=0
        for answere in quizanswers:
            if correctquizanswers[i]== answere:
                i+=1
        articleScore.score = i
        articleScore.done = True
        articleScore.save()
        return Response("Saved", status=status.HTTP_201_CREATED)

#################################################################################
# File part

# POST: Create a file object
# PUT: Link created file object to article
# http://127.0.0.1:7000/v1/fileupload/
class FileUpload(APIView):
    parser_classes=(FormParser, MultiPartParser,)
    def post(self, request):
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        file_serializer = FileSerializer(data={'name': request.FILES.get('myfile').name, 'file': request.FILES.get('myfile')})
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def PATCH(self,request):
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        if not checkPriveledge(request):
            return Response("Not enough priveledge", status=status.HTTP_401_UNAUTHORIZED)
        #TODO: ADD SAFETYCHECKS HERE
        article_link = ArticleLink(article=Article.objects.get(id= request.POST.get("ArticleID")),filepath=File.objects.get(id = request.POST.get("FileID")))
        article_link.save()
        return Response("Created", status=status.HTTP_201_CREATED)



# GET: get file links for a specifc article
# http://127.0.0.1:7000/v1/files/article/<id>/
class GetFileLinksByArticle(APIView):
    def get(self, request, id):
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        files = set()
        for fileLink in ArticleLink.objects.filter(article= id):
            files.add(fileLink.filePath)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

#################################################################################
# Highscores part

# GET: Get highscores for all  ???
# http://127.0.0.1:7000/v1/highscores/
class GetAllHighScores(APIView):
    def get(self, request):
        if not validate(request):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        articleScores = ArticleScore.objects.values("username").annotate(score=Sum('score')).order_by("-score")
        serializer = ArticleScoreSerializer(articleScores, many=True)
        return Response(serializer.data)

#################################################################################

def InputCheck(value):
    if value is None  or value == "" or len(value) > 25:
        return False;
    return True