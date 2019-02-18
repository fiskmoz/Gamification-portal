from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from quickstart.auth import validate
from quickstart.models import Quiz, QuizEntry
from django.utils import timezone


class Home(APIView): 
    def get(self, request, format=None): 
        if request.user.is_anonymous:
            return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        if not validate(request.user.username, request.user.password):
            return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

class Quiz(APIView): 
    def post(self, request, format=None): 
        # if request.user.is_anonymous: 
        #     return Response(data='You are not authenticated!', status=status.HTTP_400_BAD_REQUEST)
        # if not validate(request.user.username, request.user.password):
        #     return Response(data='Not authorized', status=status.HTTP_401_UNAUTHORIZED)
        # quiz = Quiz()
        myList = []
        counter = 0
        print(request.POST)
        for var in request.POST:
            if counter == 0:
                name = var;
            if counter == 1: 
                desc = var;
            if counter == 2:
                size = var;
                quiz = Quiz(QuizName=name, QuizCreator="default", Date = timezeone.now()) 
                quiz.save()
            if counter >= 8:
                quizentry = QuizEntry(QuizID = quiz.id, Question = myList[0], AlternativeA = myList[1], AlternativeB = myList[2], AlternativeC = myList[3], Correct = myList[4])
                myList.clear()
                counter = 0
                quizentry.save()
            if counter <8 and counter > 2:
                myList.append(var)
            counter = counter+1
        return Response(data="SUCCESS! :D ", status = status.HTTP_200_OK)