from django.contrib import admin
from .models import File, Quiz, QuizEntry
# Register your models here.

admin.site.register(File)
admin.site.register(Quiz)
admin.site.register(QuizEntry)