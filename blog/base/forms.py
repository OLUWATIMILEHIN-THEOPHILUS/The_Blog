from .models import User, Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email',
                  'password1', 'password2', 'avatar']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fiels = '__all__'

        exclude = ['writer']
