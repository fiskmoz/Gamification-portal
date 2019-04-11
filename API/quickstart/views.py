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
from datetime import timedelta

# Homepage
# http://127.0.0.1:7000/v1/
class Home(APIView): 
    def get(self, request, format=None): 
        if request.user.is_anonymous:
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        if not validate(request.user.username, request.user.password):
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
        quizes = Quiz.objects.all()
        serializer = QuizSerializer(quizes, many = True)
        return Response(serializer.data)

    def post(self, request, format=None): 
        name = request.POST.get("Quizname")
        desc = request.POST.get("Description")
        creator = request.POST.get("Creator")
        if name == "":
            return
        quiz = Quiz(name=name, description = desc , creator = creator) 
        quiz.save() 
        myList = []
        length = int(len(request.POST))
        j = 0
        i = 0
        while i < length-2:
            myList.append(request.POST.get(str(i)))
            if j > 3 :
                quizentry = QuizEntry(quiz = quiz, question = myList[0], alta = myList[1], altb = myList[2], altc = myList[3], correct = myList[4])
                myList.clear()
                j = 0
                i += 1
                quizentry.save()
                continue
            i += 1
            j += 1
        return Response(data="SUCCESS! :D ", status = status.HTTP_200_OK)


# GET: Get an entire quiz by article ID.
# http://127.0.0.1:7000/v1/news/quiz/<id>/
class GetQuizByArticleId(APIView):
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
        news = Article.objects.all().order_by("-date")
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        quizID = request.POST.get("ArticleQuiz")
        Title = request.POST.get("ArticleTitle")
        Description = request.POST.get("ArticleDescription")
        ShortDesc = request.POST.get("ArticleShortDescription")
        creator = request.POST.get("Creator")
        if Title == "":
            return
        article = Article(title=Title, description=Description, subtitle = ShortDesc, date = timezone.now(), creator= creator)
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
        user = request.GET.get('User') 
        article = Article.objects.get(id= id)
        done = False
        try:
            articleScore = ArticleScore.objects.get(article=article, username= user)
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
        articleID = request.POST.get('ArticleID') 
        creator = request.POST.get('Creator')
        article = Article.objects.get(id = articleID)
        try:
            articleScore = ArticleScore.objects.get(article = article, username = creator)
        except:
            articleScore = ArticleScore(username = creator, article=article, score=0, done=False ,date= timezone.now())
        print(articleScore)
        if articleScore.done is True:
            return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if articleScore.started is False:
            articleScore.started = True
            articleScore.save()
        return Response("", status=status.HTTP_200_OK)

    def patch(self, request, id, *args, **kwargs):
        # TODO: ADD SAFETYCHECKS FOR THESE!
        article = Article.objects.get(id = request.POST.get('articleID'))
        articleScore = ArticleScore.objects.get(article = article, username=request.POST.get('Creator'))
        time = timezone.now() - articleScore.date
        if time > timedelta(seconds= 600):
            articleScore.done = True
            articleScore.save()
        if articleScore.done:
            return Response("Saved", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        i=0
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
        file_serializer = FileSerializer(data={'name': str(file), 'file': request.FILES.get('myfile')})
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        #TODO: ADD SAFETYCHECKS HERE
        article_link = ArticleLink(article=Article.objects.get(id= request.POST.get("ArticleID")),filepath=File.objects.get(id = request.POST.get("FileID")))
        article_link.save()
        return Response("Created", status=status.HTTP_201_CREATED)



# GET: get file links for a specifc article
# http://127.0.0.1:7000/v1/news/quiz/files/
class GetFileLinksByArticle(APIView):
    def get(self, request, id):
        files = set()
        for fileLink in ArticleLink.objects.filter(article= id):
            files.add(fileLink.filePath)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

#################################################################################