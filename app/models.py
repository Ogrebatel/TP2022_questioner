from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import BaseUserManager
import datetime

from django.db.models import Count
from django.utils import timezone


class ProfileManager(UserManager):

    def create_profile(self, avatar=None, **extra_fields):
        user = self.create_user(**extra_fields)
        if user:
            user.avatar = avatar
            user.save()
        return user


    def get_active_users(self):
        return self.annotate(answers_count=Count('answers')).order_by('-answers_count')



class Profile(AbstractUser):
    avatar = models.ImageField(default='1.png')
    objects = ProfileManager()

class TagManager(models.Manager):
    def get_hot_tags(self):
        return self.annotate(question_count=Count('questions')).order_by('-question_count')

class Tag(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    objects = TagManager()

    def __str__(self):
        return f'tag: {self.name}'


class QuestionManager(models.Manager):
    def get_newest(self):
        return self.order_by('-datetime')

    def get_questions_by_tag(self, tag):
        return self.filter(tags__name=tag).order_by('-datetime')

    def get_hot_questions(self):
        return self.annotate(like_count=Count('likes')).order_by('-like_count')

    def get_answers(self):
        return self.answers.annotate(like_count=Count('likes')).order_by('-like_count')


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100)
    text = models.TextField()
    answers_number = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='tags', related_query_name='questions')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return f'Question: {self.title}'


class AnswerManager(models.Manager):
    def get_sorted_questions(self):
        return self.annotate(like_count=Count('likes')).order_by('-like_count')

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    objects = AnswerManager()

    def __str__(self):
        return f'Answer {self.answer_id}'


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    toAnswer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes', null=True)
    toQuestion = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes', null=True)
