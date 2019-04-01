from django.db import models
from django.utils import timezone

class Quiz(models.Model): 
    id = models.AutoField(max_length=250, primary_key=True)
    QuizName = models.CharField(max_length=250)
    QuizCreator = models.CharField(max_length=250)
    Description = models.CharField(max_length = 4000, default = "")
    date = models.CharField(max_length=100, default = timezone.now())

    def __str__(self):
        return str(self.QuizName)

class QuizEntry(models.Model):
    QuizID = models.ForeignKey(Quiz, to_field='id', on_delete=models.CASCADE, default=None)
    Question = models.CharField(max_length=250)
    AlternativeA = models.CharField(max_length=250)
    AlternativeB = models.CharField(max_length=250)
    AlternativeC = models.CharField(max_length=250)
    Correct = models.CharField(max_length=250)

    def __str__(self):
        return "Question for: " + str(self.QuizID)

class File(models.Model):
    id = models.AutoField(max_length=250, primary_key=True)
    name = models.CharField(max_length=250)
    file = models.FileField(upload_to="files/", unique=True, blank=False, null=False, default="UNDEFINED")

    def __str__(self):
        return self.name

class Article(models.Model):
    id = models.AutoField(max_length=250, primary_key=True)
    title = models.CharField(max_length=100)
    date = models.CharField(max_length=100, default = timezone.now())
    description = models.CharField(max_length=4000)
    shortDescription = models.CharField(max_length= 300, default = "A description")

    def __str__(self):
        return str(self.title)

class ArticleLink(models.Model):
    id = models.AutoField(max_length=250, primary_key=True)
    article = models.ForeignKey(Article, to_field="id", on_delete=models.CASCADE, default=None)   
    filePath = models.ForeignKey(File, to_field="file", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "File for: " + str(self.article)

class QuizLink(models.Model):
    id = models.AutoField(max_length=250, primary_key=True)
    article = models.ForeignKey(Article, to_field="id", on_delete=models.CASCADE, default=None) 
    quiz = models.ForeignKey(Quiz, to_field="id", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.quiz) +" --- "+ str(self.article)