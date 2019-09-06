import re

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model, login, authenticate, logout
from .forms import SignUpForm


User = get_user_model()

# 사용자 회원가입
def user_signup(request):
    # Class Based View -> dispatch -> get, post
    if request.is_ajax():
        if request.POST.get('id') == "":
            return JsonResponse({'noId':True})
        elif request.POST.get('realName') == "":
            return JsonResponse({'noRealName':True})
        elif request.POST.get('password') == "":
            return JsonResponse({'noPassword':True})
        elif request.POST.get('password2') == "":
            return JsonResponse({'noPassword2':True})


        # username 길이가 10자리 초과한 경우
        signup_id = request.POST.get('id')
        if len(signup_id) > 15:
            return JsonResponse({'tooLongId':True})


        # id에 한글 혹은 특수문자 포함되어 있는 경우
        hangul = re.compile('[가-힣]')
        symbol = re.compile('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]')
        if re.search(hangul, signup_id) or re.search(symbol, signup_id):
            return JsonResponse({'wrongId':True})


        # 이미 등록된 id인 경우
        if User.objects.filter(username=request.POST.get('id')).exists():
            return JsonResponse({'idExists':True})

        # realName에 영문자, 숫자, 특수문자가 존재하는 경우
        wrong_str = re.compile('[a-zA-Z0-9-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]')
        if wrong_str.search(request.POST.get('realName')):
            return JsonResponse({'wrongName':True})

        # realName이 5자리 초과한 경우
        if len(request.POST.get('realName')) > 5:
            return JsonResponse({'tooLongName':True})

        # password2와 password가 일치하지 않는 경우
        if request.POST.get('password') != request.POST.get('password2'):
            return JsonResponse({'notMatch':True})

        # password가 비밀번호 형식에 적합하지 않은 경우 (8자리이상 & 영어 소문자/대문자/특수문자/숫자 중 3개 이상 조합)
        password = request.POST.get('password')
        if len(password) < 8:
            return JsonResponse({'shortLength':True})
        lower_case = re.compile('[a-z]')
        higher_case = re.compile('[A-Z]')
        number = re.compile('[0-9]')
        symbol = re.compile('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]')

        i = 0
        count = 0
        if re.search(lower_case, password):
            count += 1
        if re.search(higher_case, password):
            count += 1
        if re.search(number, password):
            count += 1
        if re.search(symbol, password):
            count += 1
        # 문자 조합이 3가지 미만일 경우
        if count < 3:
            return JsonResponse({'wrongCombination':True})


        # 사용자가 작성한 회원가입 내용 형식이 적상인 경우
        real_name = request.POST.get('realName')
        id = request.POST.get('id')
        password = request.POST.get('password')

        user = User(last_name = real_name[0], first_name=real_name[1:], username=id)
        user.set_password(password)
        user.save()

        return JsonResponse({'works':True})

    return JsonResponse({'notValid':True})


# 사용자 로그인
def user_login(request):
    if request.is_ajax():
        # 이메일 주소를 입력하지 않은 경우
        if request.POST.get('id')=="" :
            return JsonResponse({'noId':True})

        # 비밀번호를 입력하지 않은 경우
        elif request.POST.get('password')=="":
            return JsonResponse({'noPassword':True})

        id = request.POST.get('id')
        password = request.POST.get('password')
        user = authenticate(username=id, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'works':True})
        return JsonResponse({'wrongInformation':True})

    return JsonResponse({'notAjax':True})


# 사용자 로그아웃
def user_logout(request):
    if request.is_ajax():
        logout(request)
        return JsonResponse({'works':True})

    return JsonResponse({'notAjax':True})
