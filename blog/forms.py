from django.contrib.auth.models import User
from django.conf import settings
from django import forms

from .models import Profile, Post


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password']:
                raise forms.ValidationError('password don\'t match.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth',)


class CommentForm(forms.Form):
    comment_text = forms.CharField(max_length=5000, widget=forms.Textarea)

    def clean_comment_text(self):
        comment_text = self.cleaned_data['comment_text']
        if len(comment_text) > 5000:
            raise forms.ValidationError("comment is too long")
        return comment_text


class PostUpload(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'status', 'image')
