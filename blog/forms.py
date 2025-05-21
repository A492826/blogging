from django import forms
from .models import ContactMessage
from .models import Comment
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class CommentForm(forms.ModelForm):
    class Meta:   
        model = Comment
        fields = ['name', 'email', 'subject', 'message']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  # optional

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')