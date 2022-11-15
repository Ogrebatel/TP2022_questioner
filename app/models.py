from django.db import models
from django.contrib.auth.models import User
import datetime

from django.db.models import Count
from django.utils import timezone




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='1.png')


class Tag(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

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
    tags = models.ManyToManyField(Tag, related_name='questions', related_query_name='tags')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return f'Question: {self.title}'


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f'Answer {self.answer_id}'


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    toAnswer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes', null=True)
    toQuestion = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes', null=True)
