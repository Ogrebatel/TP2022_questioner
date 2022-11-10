from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from . import models
# Create your views here.

@require_GET
def index(request):
    context = {'questions': models.QUESTIONS, 'isAuth': True}
    return render(request, 'index.html', context=context)

@require_GET
def question(request, id: int):
    context = {'question': models.QUESTIONS[id]}
    return render(request, 'question.html', context=context)

@require_GET
def login(request):
    return render(request, 'login.html')

@require_GET
def signup(request):
    return render(request, 'signup.html')

@require_GET
def settings(request):
    context = {'isAuth': True}
    return render(request, 'settings.html', context=context)

@require_GET
def ask(request):
    return render(request, 'ask.html')