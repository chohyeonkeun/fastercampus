# 모델 폼을 만들려면, 2가지가 필요하다.
# 제네릭 뷰를 만들려면, 제네릭 뷰, 모델이 필요하다.
# 모델 폼을 만들려면, 모델, 폼

from django.contrib.auth.models import User

from django import forms

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput)
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput)

    class Meta:
        model = User
        # fields 에는 해당 모델에 대해 입력받을 필드들을 나열한다.
        # + 추가 필드도 포함될 수 있다. ->  필드목록과 추가 필드가 겹치면 오버라이드
        # fields에 작성한 순서대로 출력된다.
        fields = ['username', 'password', 'password2', 'email']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['email'].label = '이메일 주소'


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        # 항상 해당 필드의 값을 리턴한다.
        return cd['password']
