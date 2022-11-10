from django.db import models

QUESTIONS = [
    {
        'id': question_id,
        'title': f'Question #{question_id}',
        'text': f'Text of question #{question_id}',
        'answersNumber': question_id * question_id,
        'tags': [f'tag{i}' for i in range(question_id + 1)]
    } for question_id in range(30)
]


ANSWERS = [
    {
        'question_id': question_id,
        'answers': [
            {
                'answer_id': answer_id,
                'text': f'answer with number {answer_id} to the question {question_id}',
            } for answer_id in range (question_id)
        ]
    } for question_id in range(30)
]

TAGS = [



]
