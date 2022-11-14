from django.db import models
from django.contrib.auth.models import User
import datetime

from django.utils import timezone


class Profile(User):
    avatar = models.ImageField(default='1.png')

class Tag(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    def __str__(self):
        return f'tag: {self.name}'

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='like')


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=50)
    text = models.TextField()
    answers_number = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='questions', related_query_name='tags')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return f'Question: {self.title}'


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')







