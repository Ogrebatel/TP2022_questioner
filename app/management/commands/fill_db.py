import random
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from faker import Faker
from app import models


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help=u'ratio')

    def gen_tags(self, ratio):
        fake = Faker()
        models.Tag.objects.bulk_create(
            [models.Tag(name=get_random_string(10)) for i in range(ratio)]
        )

    def gen_profiles(self, ratio):
        fake = Faker()
        # models.Profile.objects.bulk_create(
        #     [models.Profile(username=fake.name(),
        #                          email=fake.email(),
        #                          password=fake.word()
        #                     ) for i in range(ratio)]
        # )
        for i in range(ratio):
            models.Profile.objects.create(username=fake.name(),
                           email=fake.email(),
                           password=fake.word()
                           ).save()
    def gen_random_text(self):
        rand_text = str()
        for j in range(random.randint(0, 100)):
            rand_text = rand_text + ' ' + get_random_string(10)
        return rand_text

    def gen_questions(self, ratio):
        fake = Faker()
        profile_objs = models.Profile.objects.all()
        tag_objs = models.Tag.objects.all()

        models.Question.objects.bulk_create(
            [models.Question(title=fake.sentence(),
                             text=fake.text(),
                             user=profile_objs[random.randint(0, profile_objs.count() - 1)]
                             ) for i in range(ratio)]
        )

        questions = models.Question.objects.all()
        for question in questions:
            question.tags.set(random.choices(tag_objs, k=3))  # я понимаю, что теги могут повториться, но
                                                                  # ManyToMany отработает корректно, и повторяющихся
                                                                  # тэгов не будет.
            question.save()

    def gen_answers(self, ratio):
        fake = Faker()
        question_objs = models.Question.objects.all()
        profile_objs = models.Profile.objects.all()
        models.Answer.objects.bulk_create(
            [models.Answer(text=fake.text(),
                          user=profile_objs[random.randint(0, profile_objs.count() - 1)],
                          question=question_objs[random.randint(0, question_objs.count() - 1)]) for i in range(ratio)]
        )


    def gen_likes(self, ratio):
        question_objs = models.Question.objects.all()
        profile_objs = models.Profile.objects.all()
        answer_objs = models.Answer.objects.all()
        models.Like.objects.bulk_create(
            [models.Like(user=profile_objs[random.randint(0, profile_objs.count() - 1)],
                         toQuestion=question_objs[random.randint(0, question_objs.count() - 1)]) for i in range(ratio)]
        )

        models.Like.objects.bulk_create(
            [models.Like(user=profile_objs[random.randint(0, profile_objs.count() - 1)],
                         toAnswer=answer_objs[random.randint(0, answer_objs.count() - 1)]) for i in range(ratio)]
        )

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        self.gen_tags(ratio)
        self.gen_profiles(ratio)
        self.gen_questions(ratio * 10)
        self.gen_answers(ratio * 100)
        self.gen_likes(ratio * 200)
