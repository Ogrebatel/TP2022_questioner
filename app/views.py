from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

# Create your views here.

@require_GET
def index(request):
    return render(request, 'index.html')

def question(request, question_id: int):
    return HttpResponse(f'question id = {question_id}')