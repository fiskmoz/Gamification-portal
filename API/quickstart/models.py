from django.db import models
from django.utils import timezone

class Quiz(models.Model): 
    QuizName = models.CharField(max_length=250)
    QuizCreator = models.CharField(max_length=250)
    Date = models.CharField(max_length=250, default=timezone.now())

class QuizEntry(models.Model):
    QuizID = models.ForeignKey(Quiz, to_field='id', on_delete=models.CASCADE, default=None)
    Question = models.CharField(max_length=250)
    AlternativeA = models.CharField(max_length=250)
    AlternativeB = models.CharField(max_length=250)
    AlternativeC = models.CharField(max_length=250)
    Correct = models.CharField(max_length=250)

class File(models.Model):
    name = models.CharField(max_length=250)
    file = models.FileField(upload_to="files/", blank=False, null=False, default="UNDEFINED")

    def __str__(self):
        return self.name + ": " + str(self.file)