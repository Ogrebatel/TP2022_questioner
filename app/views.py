from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET
from . import models
# Create your views here.

@require_GET
def index(request):
    questions = models.Question.objects.order_by('-datetime')
    paginator = Paginator(questions, 5)
    pageNumber = request.GET.get('page')
    curPage = paginator.get_page(pageNumber)
    context = {'objList': curPage, 'isAuth': True, 'paginator': paginator}
    return render(request, 'index.html', context=context)

@require_GET
def question(request, id: int):

    question = models.Question.objects.get(question_id=id)
    answers = question.answers.all()
    paginator = Paginator(answers, 3)

    answersPageNumber = request.GET.get('page')
    curPage = paginator.get_page(answersPageNumber)

    context = {'question': question, 'objList': curPage, 'paginator': paginator}
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
    questions = models.Question.objects.filter(tags__name=tag).order_by('-datetime')

    paginator = Paginator(questions, 5)
    pageNumber = request.GET.get('page')
    curPage = paginator.get_page(pageNumber)
    context = {'objList': curPage, 'paginator': paginator, 'tag': tag}
    return render(request, 'tags.html', context=context)