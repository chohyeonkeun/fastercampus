from django import forms
from .models import Document, Comment

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['category', 'title', 'text', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = "댓글"
        self.fields['text'].widget = forms.TextInput()
        self.fields['text'].widget.attrs = {'class':"form-control", 'placeholder':"댓글을 입력하세요"}
