from django.contrib import auth
from django.contrib.auth import logout

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from . import models
from .forms import LoginForm, RegistrationForm, QuestionForm, AnswerForm, SettingsForm
from .internals import make_pagination, gen_base_context
from .models import Question, Like, Answer, Dislike


def index(request):
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
    if request.user.is_authenticated:
        if request.method == 'GET':
            answer_form = AnswerForm(request.user, question)
            context['form'] = answer_form
        if request.method == 'POST':
            answer_form = AnswerForm(request.user, question, request.POST)
            context['form'] = answer_form
            if answer_form.is_valid():
                answer = answer_form.save()
                if answer:
                    return redirect("/question/" + str(question.question_id))
                else:
                    answer_form.add_error(field=None, error="internal error")

    return render(request, 'question.html', context=context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))
    context = gen_base_context(request)
    if request.method == 'GET':
        redirect_name = request.GET.get('continue', False)
        if redirect_name:
            auth.REDIRECT_FIELD_NAME = redirect_name
        user_form = LoginForm()
        context['form'] = user_form
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        context['form'] = user_form
        if user_form.is_valid():
            user = auth.authenticate(request=request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                if auth.REDIRECT_FIELD_NAME != 'next':
                    return redirect(auth.REDIRECT_FIELD_NAME)
                else:
                    return redirect(reverse("index"))
            else:
                user_form.add_error(field=None, error="Wrong username or password!")

    return render(request, 'login.html', context=context)


@login_required(redirect_field_name='login')
def logout_view(request):
    auth.REDIRECT_FIELD_NAME = 'index'
    logout(request)
    return redirect('index')


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
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
                return redirect(reverse('login'))
            else:
                user_form.add_error(field=None, error="User with the same username exists!")

    return render(request, 'signup.html', context=context)


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def settings(request):
    context = gen_base_context(request)

    if request.method == 'GET':
        settings_form = SettingsForm(request.user)
        context['form'] = settings_form

    if request.method == 'POST':
        settings_form = SettingsForm(request.user, request.POST, request.FILES)
        context['form'] = settings_form
        if settings_form.is_valid():
            settings_form.save()
    return render(request, 'settings.html', context=context)


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def ask(request):
    sad = str

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


@require_POST
@login_required(login_url="login")
def like_view(request):
    object_id = request.POST['object_id']
    object_type = request.POST['object_type']

    if object_type == 'Question':
        object = Question.objects.get(question_id=object_id)
        try:
            like = Like.objects.get(user=request.user, toQuestion=object)
        except Like.DoesNotExist:
            like = None

        if (like):
            like.delete()
        else:
            Like.objects.create(user=request.user, toQuestion=object)
            try:
                dislike = Dislike.objects.get(user=request.user, toQuestion=object)
            except Dislike.DoesNotExist:
                dislike = None

            if (dislike):
                dislike.delete()

    if object_type == 'Answer':
        object = Answer.objects.get(answer_id=object_id)
        try:
            like = Like.objects.get(user=request.user, toAnswer=object)
        except Like.DoesNotExist:
            like = None

        if (like):
            like.delete()
        else:
            Like.objects.create(user=request.user, toAnswer=object)
            try:
                dislike = Dislike.objects.get(user=request.user, toAnswer=object)
            except Dislike.DoesNotExist:
                dislike = None

            if (dislike):
                dislike.delete()

    object.total_like_count = object.likes.count() - object.dislikes.count()
    object.save()

    return JsonResponse({
        'status': 'ok',
        'likes_count': object.total_like_count
    })

@require_POST
@login_required(login_url="login")
def dislike_view(request):
    object_id = request.POST['object_id']
    object_type = request.POST['object_type']

    if object_type == 'Question':
        object = Question.objects.get(question_id=object_id)
        try:
            dislike = Dislike.objects.get(user=request.user, toQuestion=object)
        except Dislike.DoesNotExist:
            dislike = None

        if (dislike):
            dislike.delete()
        else:
            Dislike.objects.create(user=request.user, toQuestion=object)
            try:
                like = Like.objects.get(user=request.user, toQuestion=object)
            except Like.DoesNotExist:
                like = None

            if (like):
                like.delete()

    if object_type == 'Answer':
        object = Answer.objects.get(answer_id=object_id)
        try:
            dislike = Dislike.objects.get(user=request.user, toAnswer=object)
        except Dislike.DoesNotExist:
            dislike = None

        if (dislike):
            dislike.delete()
        else:
            Dislike.objects.create(user=request.user, toAnswer=object)
            try:
                like = Like.objects.get(user=request.user, toAnswer=object)
            except Like.DoesNotExist:
                like = None

            if (like):
                like.delete()

    object.total_like_count = object.likes.count() - object.dislikes.count()
    object.save()

    return JsonResponse({
        'status': 'ok',
        'likes_count': object.total_like_count
    })
