from django.contrib import admin
from .models import File, Quiz, QuizEntry, Article, QuizLink, ArticleLink
# Register your models here.

admin.site.register(File)
admin.site.register(Quiz)
admin.site.register(QuizEntry)
admin.site.register(Article)
admin.site.register(QuizLink)
admin.site.register(ArticleLink)