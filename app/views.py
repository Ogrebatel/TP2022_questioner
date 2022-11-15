from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from . import models


# Create your views here.

def make_pagination(request, objects):
    paginator = Paginator(objects, 5)
    pageNumber = request.GET.get('page')
    curPage = paginator.get_page(pageNumber)
    return {'objList': curPage, 'paginator': paginator}


@require_GET
def index(request):
    questions = models.Question.objects.get_newest()
    context = {'isAuth': True}
    context.update(make_pagination(request, questions))
    return render(request, 'index.html', context=context)


@require_GET
def question(request, id: int):
    question = get_object_or_404(models.Question, question_id=id)
    answers = question.answers.annotate(like_count=Count('likes')).order_by('-like_count') # я не смог придумать через
                                                                                           # manager
    context = {'question': question}
    context.update(make_pagination(request, answers))
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


@require_GET
def tags(request, tag):
    questions = models.Question.objects.get_questions_by_tag(tag)
    context = {'tag': tag}
    context.update(make_pagination(request, questions))
    return render(request, 'tags.html', context=context)


@require_GET
def best(request):
    questions = models.Question.objects.get_hot_questions()
    context = {'isAuth': True}
    context.update(make_pagination(request, questions))
    return render(request, 'best.html', context=context)
