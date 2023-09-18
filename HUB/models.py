from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    ...


class Articles(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    link = models.URLField()
    photo = models.ImageField(upload_to='HUB/files/photos/', null=True, blank=True)

    def __str__(self):
        return self.name
 

class ResearchPaper(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    link = models.URLField()
    photo = models.ImageField(upload_to='HUB/files/photos/', null=True, blank=True)

    def __str__(self):
        return self.name
    

class QuizQuestion(models.Model):
    research_paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text
    
    
class ArticleQuestion(models.Model):
    research_paper = models.ForeignKey(Articles, on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text
    
class chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_text = models.TextField()
    text_at = models.DateTimeField(auto_now_add=True)