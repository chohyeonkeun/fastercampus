from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from .forms import SignUpForm


User = get_user_model()

def signup(request):
    # Class Based View -> dispatch -> get, post
    if request.method == "POST":
        # Todo : 입력받은 내용을 이용해서 회원 객체 생성
        # 입력받은 내용 확인하기
        # 모델 폼을 이용해서 코드를 간결하게 바꾼다.
        signup_form = SignUpForm(request.POST)
        # form validation
        if signup_form.is_valid():
            # 1. 저장하고 인스턴스 생성
            user_instance = signup_form.save(commit=False)
            # 2. 패스워드 암호화 -> 저장
            # 폼이 가지고 있는 cleaned_data란? : 유효한 문자만 남긴 상태로 처리 과정을 거친 데이터
            user_instance.set_password(signup_form.cleaned_data['password'])
            user_instance.save()
            return render(request, 'accounts/signup_complete.html', {'username': user_instance.username})
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        # email = request.POST.get('email')

        # 회원 객체 생성하기
        # user = User()
        # user.username = username
        # user.set_password(password)
        # user.first_name = first_name
        # user.last_name = last_name
        # user.email = email
        # user.save()


    else:
        # Todo : form 객체를 만들어서 전달
        signup_form = SignUpForm()
        # context_values = {'form':signup_form}
        # 템플릿 연동 순
        # 1. 템플릿 불러오기
        # 2. 템플릿 렌더링하기
        # 3. HTTP Response하기
    return render(request, 'accounts/signup.html', {'form':signup_form})
