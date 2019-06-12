from django import forms
from .models import Comment, Program

class CommentForm(forms.ModelForm):
    # text = forms.TextInput(label='댓글')
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # detail 페이지에서 보여지는 이름을 원래 필드글명인 'text'에서 '댓글'로 변경
        self.fields['text'].label = ''
        self.fields['text'].widget = forms.TextInput()
        self.fields['text'].widget.attrs = {"class": "form-control", "placeholder": "댓글을 입력하세요."}



class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'teacher', 'time']