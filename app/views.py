from django.contrib import auth
from django.contrib.auth import logout

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from . import models
from .forms import LoginForm, RegistrationForm, QuestionForm
from .internals import make_pagination, gen_base_context


def index(request):
    if request.user.is_authenticated:
        print(type(request.user))
    else:
        print("NOOOOOOOOOOOOO")
    context = gen_base_context(request)
    questions = models.Question.objects.get_newest()
    context.update({'isAuth': True})
    context.update(make_pagination(request, questions))
    return render(request, 'index.html', context=context)


def question(request, id: int):
    context = gen_base_context(request)
    question = get_object_or_404(models.Question, question_id=id)
    answers = question.answers.get_sorted_questions()
    context.update({'question': question})
    context.update(make_pagination(request, answers))
    return render(request, 'question.html', context=context)



def login(request):
    context = gen_base_context(request)
    if request.method == 'GET':
        user_form = LoginForm()
        context['form'] = user_form
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        context['form'] = user_form
        if user_form.is_valid():
            user = auth.authenticate(request=request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse("index"))
            else:
                user_form.add_error(field=None, error="Wrong username or password:")

    return render(request, 'login.html', context=context)


@login_required(redirect_field_name='login')
def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    context = gen_base_context(request)

    if request.method == 'GET':
        user_form = RegistrationForm()
        context['form'] = user_form
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST, request.FILES)
        context['form'] = user_form
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="User with the same username exists!")

    return render(request, 'signup.html', context=context)


@login_required(login_url='login')
def settings(request):
    context = gen_base_context(request)
    return render(request, 'settings.html', context=context)


@login_required(login_url='login')
def ask(request):
    context = gen_base_context(request)

    if request.method == 'GET':
        question_form = QuestionForm(request.user)
        context['form'] = question_form
    if request.method == 'POST':
        question_form = QuestionForm(request.user, request.POST)
        context['form'] = question_form
        if question_form.is_valid():
            question = question_form.save()
            if question:
                return redirect("/question/" + str(question.question_id))
            else:
                question_form.add_error(field=None, error="User with the same username exists!")

    return render(request, 'ask.html', context=context)


@require_GET
def tags(request, tag):
    context = gen_base_context(request)
    questions = models.Question.objects.get_questions_by_tag(tag)
    context.update({'tag': tag})
    context.update(make_pagination(request, questions))
    return render(request, 'tags.html', context=context)


@require_GET
def best(request):
    context = gen_base_context(request)
    questions = models.Question.objects.get_hot_questions()
    context.update({'isAuth': True})
    context.update(make_pagination(request, questions))
    return render(request, 'best.html', context=context)
