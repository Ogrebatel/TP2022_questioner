from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from app.models import Profile


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
        fields = ('username', 'email', 'password', 'password_check', 'first_name', 'last_name', 'avatar')

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
            w, h = get_image_dimensions(avatar)

            max_width = max_height = 500
            if w > max_width or h > max_height:
                raise ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

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
