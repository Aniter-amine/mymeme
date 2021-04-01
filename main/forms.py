from django import forms
from .models import Memes, Comment


class MemesForm(forms.ModelForm):
    class Meta:
        model = Memes
        fields = ['body', 'image', 'video']

        widgets = {
            'body': forms.TextInput(attrs={'class': 'input is-primary'}),
            'image': forms.FileInput(attrs={'class': 'file-input'}),
            'video': forms.FileInput(attrs={'class': 'file-input'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': forms.Textarea(attrs={'class': 'textarea'}),
        }
