from rest_framework import serializers
from .models import File, Quiz, QuizEntry, Article

class FileSerializer(serializers.ModelSerializer):

    class Meta():
        model = File
        fields = ('__all__')

class QuizSerializer(serializers.ModelSerializer): 

    class Meta():
        model = Quiz
        fields = ('__all__')

class QuizEntrySerializer(serializers.ModelSerializer): 

    class Meta():
        model = QuizEntry
        fields = ('__all__')

class NewsSerializer(serializers.ModelSerializer):

    class Meta():
        model = Article
        fields = ('__all__')