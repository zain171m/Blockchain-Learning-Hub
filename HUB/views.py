from django.shortcuts import render

# Create your views here.
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *

from django import forms

class Pprform(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    link = forms.URLField()
    photo = forms.ImageField()

class Qzform(forms.Form):
    name = forms.CharField(max_length=255)
    question = forms.CharField(widget=forms.Textarea)
    option1 = forms.CharField()
    option2 = forms.CharField()
    option3 = forms.CharField()
    option4 = forms.CharField()
    correct = forms.CharField()




def index(request):
        Papers = ResearchPaper.objects.all()
        if len(Papers) == 1:
            paper_pairs = [[Papers[0]]]  # Create a list containing a single pair with the single object
        else:
            paper_pairs = [Papers[i:i + 2] for i in range(0, len(Papers), 2)]

        articles = Articles.objects.all()
        if len(articles) == 1:
            art_pairs = [[articles[0]]]  # Create a list containing a single pair with the single object
        else:
            art_pairs = [articles[i:i + 2] for i in range(0, len(articles), 2)]



        return render(request, "HUB/main.html", {'paper_pairs' : paper_pairs, 'Papers' : Papers, 'art_pairs' : art_pairs, 'articles' : articles})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "HUB/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "HUB/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        # Attempt to create new user
        try:
            user = ResearchPaper.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "HUB/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "HUB/register.html")

def quiz(request, id, type):
    return render(request, "HUB/quiz.html", {'ResearchPaper_id': id, 'type':type })




def get_quiz_questions(request, research_paper_id):

   
    # Parse the JSON data from the request body
    data = json.loads(request.body.decode('utf-8'))

    # Access the 'type' parameter from the JSON data
    quiz_type = data.get('type', '')


    if quiz_type == "Article":
        # Query the QuizQuestion model to retrieve quiz questions for the specified research paper
        quiz_questions = ArticleQuestion.objects.filter(research_paper__id=research_paper_id).values(
            'id', 'research_paper__name', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option'
        )

    else:
        quiz_questions = QuizQuestion.objects.filter(research_paper__id=research_paper_id).values(
        'id', 'research_paper__name', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option'
        )

    # Convert the query result to a list
    quiz_questions_list = list(quiz_questions)

    # Return the quiz questions as JSON response
    return JsonResponse({'quiz_questions': quiz_questions_list})



@csrf_exempt
@login_required
def ppr_update(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    form = Pprform(request.POST, request.FILES)  # Include request.FILES to handle file uploads
    if form.is_valid():
        # Access the uploaded file using form.cleaned_data['photo']
        # Access the form fields
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        link = form.cleaned_data['link']

        # Access the uploaded photo
        uploaded_photo = form.cleaned_data['photo']
        # Process the form data and the uploaded photo as needed

        try:
            new_paper = ResearchPaper(
                    name = name,
                    description = description,
                    link = link
                )
            new_paper.photo = uploaded_photo
            new_paper.save()
        except IntegrityError:
            return JsonResponse({'error': 'Paper is already saved'})
        
        return JsonResponse({'message': 'Data saved successfully'})
    else:
        return JsonResponse({'error': 'Form is not valid'})

"""
    data = json.loads(request.body)

    # Get contents of post
    id = data.get("post_id", "")
    updtd_text = data.get("post_text", "")

    post = Post.objects.get(pk = id)

    post.text = updtd_text
    post.save()

    #return JsonResponse({"message": "Post Updated successfully."}, status=201)
    return JsonResponse(post.serialize())
"""

@csrf_exempt
@login_required
def qz_update(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    form = Qzform(request.POST, request.FILES)  # Include request.FILES to handle file uploads
    if form.is_valid():
        # Access the uploaded file using form.cleaned_data['photo']
        # Access the form fields
        name = form.cleaned_data['name']
        question = form.cleaned_data['question']
        option1 = form.cleaned_data['option1']
        option2 = form.cleaned_data['option2']
        option3 = form.cleaned_data['option3']
        option4 = form.cleaned_data['option4']
        correct = form.cleaned_data['correct']

        paper = ResearchPaper.objects.get(name = name)

        try:
            new_qz = QuizQuestion(
                    research_paper = paper,
                    question_text = question,
                    option1 = option1,
                    option2 = option2,
                    option3 = option3,
                    option4 = option4,
                    correct_option = correct,

                )
            new_qz.save()
        except IntegrityError:
            return JsonResponse({'error': 'Quiz is already saved'})
        
        return JsonResponse({'message': 'Data saved successfully'})
    else:
        return JsonResponse({'error': 'Form is not valid'})




@csrf_exempt
@login_required
def art_update(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    form = Pprform(request.POST, request.FILES)  # Include request.FILES to handle file uploads
    if form.is_valid():
        # Access the uploaded file using form.cleaned_data['photo']
        # Access the form fields
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        link = form.cleaned_data['link']

        # Access the uploaded photo
        uploaded_photo = form.cleaned_data['photo']
        # Process the form data and the uploaded photo as needed

        try:
            new_paper = Articles(
                    name = name,
                    description = description,
                    link = link
                )
            new_paper.photo = uploaded_photo
            new_paper.save()
        except IntegrityError:
            return JsonResponse({'error': 'Paper is already saved'})
        
        return JsonResponse({'message': 'Data saved successfully'})
    else:
        return JsonResponse({'error': 'Form is not valid'})

"""
    data = json.loads(request.body)

    # Get contents of post
    id = data.get("post_id", "")
    updtd_text = data.get("post_text", "")

    post = Post.objects.get(pk = id)

    post.text = updtd_text
    post.save()

    #return JsonResponse({"message": "Post Updated successfully."}, status=201)
    return JsonResponse(post.serialize())
"""

@csrf_exempt
@login_required
def artq_update(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    form = Qzform(request.POST, request.FILES)  # Include request.FILES to handle file uploads
    if form.is_valid():
        # Access the uploaded file using form.cleaned_data['photo']
        # Access the form fields
        name = form.cleaned_data['name']
        question = form.cleaned_data['question']
        option1 = form.cleaned_data['option1']
        option2 = form.cleaned_data['option2']
        option3 = form.cleaned_data['option3']
        option4 = form.cleaned_data['option4']
        correct = form.cleaned_data['correct']

        paper = Articles.objects.get(name = name)

        try:
            new_qz = ArticleQuestion(
                    research_paper = paper,
                    question_text = question,
                    option1 = option1,
                    option2 = option2,
                    option3 = option3,
                    option4 = option4,
                    correct_option = correct,

                )
            new_qz.save()
        except IntegrityError:
            return JsonResponse({'error': 'Quiz is already saved'})
        
        return JsonResponse({'message': 'Data saved successfully'})
    else:
        return JsonResponse({'error': 'Form is not valid'})


@csrf_exempt
@login_required
def Chat(request):
    if request.method == "POST":
        message = request.POST.get('message') 
        user = request.user
        new_chat = chat(
                    user = user,
                    chat_text = message
                )
        new_chat.save()
        chats = chat.objects.all()
        return render(request, "HUB/chat.html", {'chats':chats})
    else:
        chats = chat.objects.all()
        return render(request, "HUB/chat.html", {'chats':chats})