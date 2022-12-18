from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from app.models import Profile, Question, Answer, Tag


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']

        if 'qwerty' in data:
            raise ValidationError("do not use common words in password.")

        if ' ' in data:
            raise ValidationError("do not use space symbol words in password.")

        return data


class RegistrationForm(forms.ModelForm):
    password_check = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'password_check', 'first_name', 'last_name', 'avatar']

    def clean_password_check(self):
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_check']

        if password_1 != password_2:
            raise ValidationError('Passwords are not the same')

        if " " in password_1:
            raise ValidationError('do not use space symbol words in password.')

        return password_2

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        if len(avatar) > (2000 * 1024):
            raise ValidationError(u'Avatar file size may not exceed 2M.')

        return avatar

    def clean_username(self):
        username = self.cleaned_data['username']

        if " " in username:
            raise ValidationError('do not use space symbol words in username.')

        return username

    def save(self, commit=True):
        self.cleaned_data.pop('password_check')
        return Profile.objects.create_profile(**self.cleaned_data)



class SettingsForm(forms.ModelForm):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, required=False)
    password_check = forms.CharField(min_length=8, widget=forms.PasswordInput, required=False)
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'password_check', 'avatar']

    def clean_password_check(self):
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_check']

        if password_1 != password_2:
            raise ValidationError('Passwords are not the same')

        if " " in password_1:
            raise ValidationError('do not use space symbol words in password.')

        return password_2

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar:
            if len(avatar) > (2000 * 1024):
                raise ValidationError(u'Avatar file size may not exceed 2M.')

        return avatar

    def clean_username(self):
        username = self.cleaned_data['username']

        if " " in username:
            raise ValidationError('do not use space symbol words in username.')

        return username

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False


    def save(self, commit=True):
        if self.cleaned_data['username']:
            self.user.username = self.cleaned_data['username']
        if self.cleaned_data['email']:
            self.user.email = self.cleaned_data['email']
        if self.cleaned_data['avatar']:
            self.user.avatar = self.cleaned_data['avatar']
        if self.cleaned_data['password']:
            self.user.set_password(self.cleaned_data['password'])
        return self.user.save()


class QuestionForm(forms.ModelForm):

    tags = forms.CharField(required=True)

    class Meta:
        model = Question
        fields = ['title', 'text']

    def save(self, commit=True):
        tags = str(self.cleaned_data.pop('tags')).split()
        tags_list = []
        for tag in tags:
            print(tag)
            tags_list.append(Tag.objects.get_or_create(name=tag)[0])

        self.cleaned_data['user'] = self.user
        question = Question.objects.create(**self.cleaned_data)
        if question:
            question.tags.set(tags_list)
        return question

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(QuestionForm, self).__init__(*args, **kwargs)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def save(self, commit=True):
        self.cleaned_data['question'] = self.question
        self.cleaned_data['user'] = self.user
        return Answer.objects.create(**self.cleaned_data)

    def __init__(self, user, question, *args, **kwargs):
        self.user = user
        self.question = question
        super(AnswerForm, self).__init__(*args, **kwargs)
