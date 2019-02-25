from django.contrib import admin
from .models import File, Quiz, QuizEntry, Article
# Register your models here.

admin.site.register(File)
admin.site.register(Quiz)
admin.site.register(QuizEntry)
admin.site.register(Article)