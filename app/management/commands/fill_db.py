import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.crypto import get_random_string

from app import models

class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help=u'ratio')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        for i in range(ratio):
            models.Tag(name=get_random_string(10)).save()

        for i in range(ratio):
            models.Profile(password=get_random_string(10), username=get_random_string(random.randint(10, 20))).save()

        profile_objs = models.Profile.objects.all()
        tag_objs = models.Tag.objects.all()

        for i in range(ratio):

            rand_text = str()
            for j in range(random.randint(0, 100)):
                rand_text = rand_text + ' ' + get_random_string(10)

            cur_question = models.Question(title=get_random_string(10),
                            text=rand_text,
                            user=profile_objs[random.randint(0, profile_objs.count() - 1)]
                            )
            cur_question.save()
            cur_question.tags.set(random.choices(tag_objs, k=3))    # я понимаю, что теги могут повториться, но
                                                                    # ManyToMany отработает корректно, и повтSоряющихся
                                                                    # тэгов не будет.
            cur_question.save()

        question_objs = models.Question.objects.all()

        for i in range(ratio * 10):
            rand_text = str()
            for j in range(random.randint(0, 100)):
                rand_text = rand_text + ' ' + get_random_string(10)

            cur_answer = models.Answer(text=rand_text,
                            user=profile_objs[random.randint(0, profile_objs.count() - 1)],
                            question=question_objs[random.randint(0, question_objs.count() - 1)]
                            )
            cur_answer.save()