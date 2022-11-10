from django.db import models

QUESTIONS = [
    {
        'id': id,
        'title': f'Question #{id}',
        'text': f'Text of question #{id}',
        'answersNumber': id * id,
        'tags': ['tag' for i in range(id)]
    } for id in range(30)
]
