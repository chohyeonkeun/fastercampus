from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.

from .models import Category, Program, Comment

from django.views.generic.list import ListView

from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic.base import View

from django.http import HttpResponseRedirect, Http404

from django.http import HttpResponseForbidden

from django.contrib import messages

from django.urls import reverse

from secret import naver_map

def main_page(request):
    categories = Category.objects.all()
    return render(request, 'program/main_page.html', {'object_list':categories, 'naver_id':naver_map['id']})

class Categorylist(ListView):
    model = Category
    template_name = 'category/category_list.html'

class CategoryCreate(CreateView):
    model = Category
    template_name = 'category/category_create.html'
    # permission_classes

class CategoryUpdate(UpdateView):
    model = Category
    template_name = 'category/category_update.html'
    def dispatch(self, request, *args, **kwargs):
        pass

class CategoryDetail(DetailView):
    model = Category
    template_name = 'category/category_detail.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        object = kwargs['object']
        category = object
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = category.comment_category.all()
        return context

class CategoryDelete(DeleteView):
    model = Category
    template_name = 'category/category_delete.html'

from django.shortcuts import get_list_or_404, get_object_or_404
from .forms import CommentForm
from django.template.loader import render_to_string
from django.http import JsonResponse

def comment_create(request, category_id):
    if request.user.is_anonymous:
        return JsonResponse({'notLogin':True})

    if request.is_ajax():
        category = get_object_or_404(Category, pk=category_id)
        comment_form = CommentForm(request.POST)
        comment_form.instance.nickname_id = request.user.id
        comment_form.instance.category_id = category_id
        if comment_form.is_valid():
            comment = comment_form.save()

        html = render_to_string('category/comment/comment_single.html',{'comment':comment})
        return JsonResponse({'html':html})

    raise Http404

from .models import Comment
from django.contrib import messages

def comment_delete(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    category = Category.objects.get(pk=comment.category.id)
    if request.user != comment.nickname and not request.user.is_staff:
        print(comment_id)
        messages.warning(request, "권한 없음")
        return redirect(category)

    if request.is_ajax():
        comment.delete()
        return JsonResponse({'works':True})

    if request.method == "POST":
        comment.delete()
        return redirect(category)

    raise Http404


def comment_update(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user != comment.nickname and not request.user.is_staff:
        return JsonResponse({'notAuthor':True})
    if request.is_ajax():
        form = CommentForm(request.GET, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({'works':True})
        else:
            return JsonResponse({'notValid':True})
    raise Http404

def program_list(request):
    programs = Program.objects.all()
    return render(request, 'program/program_list.html', {'object_list':programs})



from util.decorators import login_required
from django.http import HttpResponse


def program_submit(request):
    if request.is_ajax():
        obj_id_list = request.POST.getlist('obj_id_list[]')
        if request.user.is_anonymous:
            return JsonResponse({'notLogin': True})


        user = request.user
        for i in range(len(obj_id_list)):
            program_i = Program.objects.get(pk=int(obj_id_list[i]))
            for enrolled_program in user.enrolled_program.all():
                # 기존에 신청한 수업 이름과 중복 시, enrolledName True 형태로 전달
                if enrolled_program.name == program_i.name:
                    return JsonResponse({'enrolledName':True})
                # 기존에 신청한 수업 시간과 중복해서 신청했는지 확인하여 중복 시, enrolledTime True 형태로 전달
                if program_i.end_time > enrolled_program.start_time and program_i.start_time < enrolled_program.end_time:
                    return JsonResponse({'enrolledTime':True})


            # 신청할 때, 겹치는 시간대 신청했는지 확인하여 겹치는 시간대 있으면 overlaps True 형태로 전달
            if len(obj_id_list) > 1:
                if i == len(obj_id_list) - 1:
                    program_i.enroll.add(user)
                    break
                for j in range(len(obj_id_list) - i - 1):
                    j = j + i + 1
                    program_j = Program.objects.get(pk=int(obj_id_list[j]))
                    if program_i.end_time > program_j.start_time and program_i.start_time < program_j.end_time:
                        return JsonResponse({'overlaps': True})


            program_i.enroll.add(user)

        return JsonResponse({'works':True})


@login_required
def my_page(request):
    user = request.user
    enrolled_programs = user.enrolled_program.all()

    return render(request, 'program/my_page.html', {'object_list':enrolled_programs})


def enroll_delete(request):
    if request.is_ajax():
        if request.user.is_anonymous:
            return JsonResponse({'notLogin':True})

        obj_id = request.GET.get('obj_id')
        program = Program.objects.get(pk=int(obj_id))

        user = request.user
        # 사용자가 해당 수업 enroll에 있는 경우
        if user in program.enroll.all():
            program.enroll.remove(user)
            user_programs = user.enrolled_program.all()
            if not user_programs.exists():
                program_exists = False
            else:
                program_exists = True
            return JsonResponse({'works':True, 'program_exists':program_exists})



        # 이미 해당 수업 enroll에 속해있지 않은 상태
        return JsonResponse({'notEnrolled':True})
def pay_proceed(request):
    if request.is_ajax():
        # 요청한 사용자가 비로그인한 상태인 경우
        if request.user.is_anonymous:
            return JsonResponse({'notLogin':True})

        obj_id_list = request.POST.getlist('obj_id_list[]')
        for obj_id in obj_id_list:
            program = Program.objects.get(pk=int(obj_id))
            # 요청한 사용자가 이미 해당 수업을 결제한 경우
            if request.user in program.payed.all():
                return JsonResponse({'payedProgram':True})
            # 요청한 사용자가 로그인하였고, 해당 수업을 결제하지 않은 경우
            program.payed.add(request.user)
        return JsonResponse({'works':True})


def completed_hide(request):
    if request.is_ajax():
        if request.user.is_anonymous:
            return JsonResponse({'notLogin':True})

        obj_id = request.GET.get('obj_id')
        program = Program.objects.get(pk=int(obj_id))

        user = request.user
        # 사용자가 해당 수업 enroll에 있는 경우
        if user in program.enroll.all():
            program.enroll.remove(user)
            user_programs = user.enrolled_program.all()
            if not user_programs.exists():
                program_exists = False
            else:
                program_exists = True
            return JsonResponse({'works':True, 'program_exists':program_exists})

        # 이미 해당 수업 enroll에 속해있지 않은 상태
        return JsonResponse({'notEnrolled':True})


def payed_page(request):
    user = request.user
    payed_programs = user.payed_program.all()

    return render(request, 'program/payed_page.html', {'object_list': payed_programs})


def payed_delete(request):
    if request.is_ajax():
        if request.user.is_anonymous:
            return JsonResponse({'notLogin':True})

        obj_id = request.POST.get('obj_id')
        program = Program.objects.get(pk=int(obj_id))

        user = request.user

        if user in program.payed.all():
            program.payed.remove(user)
            payed_programs = user.payed_program.all()
            if not payed_programs.exists():
                program_exists = False
            else:
                program_exists = True

            return JsonResponse({'works':True, 'program_exists':program_exists})

        # 이미 해당 수업 payed에 속해있지 않은 상태
        return JsonResponse({'notPayed':True})
