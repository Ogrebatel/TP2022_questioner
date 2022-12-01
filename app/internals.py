from django.core.paginator import Paginator
from django.db import models
from . import models


def make_pagination(request, objects):
    paginator = Paginator(objects, 5)
    pageNumber = request.GET.get('page')
    curPage = paginator.get_page(pageNumber)
    return {'objList': curPage, 'paginator': paginator}

def gen_base_context(request):
    context = {'best_questions': models.Question.objects.get_hot_questions()[:5],
               'best_tags': models.Tag.objects.get_hot_tags()[:5],
               'active_users': models.Profile.objects.get_active_users()[:5]}
    return context
