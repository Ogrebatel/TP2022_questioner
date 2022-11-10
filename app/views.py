from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from . import models
# Create your views here.

@require_GET
def index(request):
    paginator = Paginator(models.QUESTIONS, 5)
    pageNumber = request.GET.get('page')
    curPage = paginator.get_page(pageNumber)
    context = {'objList': curPage, 'isAuth': True, 'paginator': paginator}
    return render(request, 'index.html', context=context)

@require_GET
def question(request, id: int):

    paginator = Paginator(models.ANSWERS[id].get("answers"), 3)
    answersPageNumber = request.GET.get('page')
    curPage = paginator.get_page(answersPageNumber)

    context = {'question': models.QUESTIONS[id], 'objList': curPage, 'paginator': paginator}
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

def tags(request, tag):
    selection = []
    for i in models.QUESTIONS:
        if tag in i.get('tags'):
            selection.append(i)

    paginator = Paginator(selection, 5)
    pageNumber = request.GET.get('page')
    curPage = paginator.get_page(pageNumber)
    context = {'objList': curPage, 'paginator': paginator, 'tag': tag}
    return render(request, 'tags.html', context=context)