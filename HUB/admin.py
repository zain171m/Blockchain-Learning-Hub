from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(ResearchPaper)
admin.site.register(QuizQuestion)
admin.site.register(Articles)
admin.site.register(ArticleQuestion)
admin.site.register(chat)


