from django.shortcuts import render, redirect

# Create your views here.

from .models import Category, Program, Schedule, Comment

from django.views.generic.list import ListView

from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic.base import View

from django.http import HttpResponseRedirect

from django.http import HttpResponseForbidden

from django.contrib import messages

from django.urls import reverse

def main_page(request):
    return render(request, 'program/main_page.html')

class Categorylist(ListView):
    model = Category
    template_name = 'category/category_list.html'

class CategoryCreate(CreateView):
    model = Category
    template_name = 'category/category_create.html'

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
   is_ajax = request.POST.get('is_ajax')

   category = get_object_or_404(Category, pk=category_id)
   comment_form = CommentForm(request.POST)
   comment_form.instance.nickname_id = request.user.id
   comment_form.instance.category_id = category_id
   if comment_form.is_valid():
       comment = comment_form.save()

   if is_ajax:
       html = render_to_string('category/comment/comment_single.html',{'comment':comment})
       return JsonResponse({'html':html})

   return redirect(category)

from .models import Comment
from django.contrib import messages

def comment_update(request, comment_id):
   is_ajax, data = (request.GET.get('is_ajax'), request.GET) if 'is_ajax' in request.GET else (request.POST.get('is_ajax', False), request.POST)

   comment = get_object_or_404(Comment, pk=comment_id)
   category = get_object_or_404(Category, pk=comment.category.id)

   if request.user != comment.nickname and not request.user.is_staff:
       messages.warning(request, "권한 없음")
       return redirect(category)

   if is_ajax:
       form = CommentForm(data, instance=comment)
       if form.is_valid():
           form.save()
           return JsonResponse({'works':True})

   if request.method == "POST":
       form = CommentForm(request.POST, request.FILES, instance=comment)
       if form.is_valid():
           form.save()
           return redirect(category)
   else:
       form = CommentForm(instance=comment)
   return render(request, 'category/comment/comment_update.html', {'form':form})

def comment_delete(request, comment_id):
   is_ajax = request.GET.get('is_ajax') if 'is_ajax' in request.GET else request.POST.get('is_ajax',False)
   comment = get_object_or_404(Comment, pk=comment_id)
   category = get_object_or_404(Category, pk=comment.category.id)

   if request.user != comment.nickname and not request.user.is_staff:
       messages.warning(request, "권한 없음")
       return redirect(category)

   if is_ajax:
       print('ajax 요청받아와서 삭제')
       comment.delete()
       return JsonResponse({"works":True})

   if request.method == "POST":
       comment.delete()
       return redirect(category)
   else:
       return render(request, 'category/comment/comment_delete.html', {'object': comment})


def program_list(request):
    programs = Program.objects.all()
    return render(request, 'program/program_list.html', {'object_list':programs})

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import ScheduleForm
@login_required
def program_submit(request):
    is_ajax = request.POST.get('is_ajax')
    program_list = Program.objects.all()
    if is_ajax:
        obj_id_list = request.POST.getlist('obj_id_list[]')
        # 수업 시간 중복해서 체크했는지 확인하여 중복 시, works가 아닌 overlaps를 데이터로 전달
        user = request.user
        schedule = Schedule.objects.filter(user=user)
        for i in range(len(obj_id_list)):
            program = program_list.get(pk=int(obj_id_list[i]))
            if schedule.filter(name=program.name).exists():
                return JsonResponse({'enrolledName': True})
            if schedule.filter(time=program.time).exists():
                return JsonResponse({'enrolledTime': True})

        for i in range(len(obj_id_list)):
            program_i = program_list.get(pk=int(obj_id_list[i]))
            if i == len(obj_id_list) - 1:
                break
            for j in range(len(obj_id_list) - i - 1):
                j = j + i + 1
                program_j = program_list.get(pk=int(obj_id_list[j]))
                if program_i.time == program_j.time:
                    return JsonResponse({'overlaps':True})


        # 수업시간 중복안했을 경우 요청한 user를 enroll 필드에 저장
        for obj_id in obj_id_list:
            program = Program.objects.get(pk=int(obj_id))
            user = request.user
            user_program = user.enrolled_program.all()
            user_program = user_program.filter(id=int(obj_id))

            if not user_program.exists():
                program.enroll.add(user)
                # 신청한 수업을 따로 schedule 모델에 저장
                schedule = Schedule(user=user ,name=program.name, teacher=program.teacher, time=program.time)
                schedule.save()
        return JsonResponse({'works':True})


@login_required
def my_page(request):
    user = request.user
    programs = user.enrolled_program.all()

    return render(request, 'program/my_page.html', {'object_list':programs})


def enroll_delete(request):
    is_ajax = request.GET.get('is_ajax') if 'is_ajax' in request.GET else request.POST.get('is_ajax',False)
    print("Test ajax", is_ajax)
    if is_ajax:
        obj_id = request.POST.get('obj_id')
        user = request.user
        program = Program.objects.get(pk=int(obj_id))
        program.enroll.remove(user)
        schedule = Schedule.objects.get(name=program.name)
        schedule.delete()

        user_program = user.enrolled_program.all()
        if not user_program.exists():
            program_exists = False
        else:
            program_exists = True
        return JsonResponse({'works':True, 'program_exists':program_exists})
