from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
import math
from .models import Document
# Create your views here.

from django.template.loader import render_to_string

from django.contrib import messages

from django.db.models import Q
from urllib.parse import urlparse
from django.http import HttpResponseRedirect, Http404


def document_list(request):

    page = int(request.GET.get('page', 1))

    paginated_by = 3
    search_type = request.GET.getlist('search_type', None)
    if not search_type:
        search_type = ['title']

    print(search_type)
    search_key = request.GET.get('search_key', None)


    search_q = None

    if search_key:
        if 'title' in search_type:
            temp_q = Q(title__icontains=search_key)
            search_q = search_q | temp_q if search_q else temp_q
        if 'author' in search_type:
            temp_q = Q(author__icontains=search_key)
            search_q = search_q | temp_q if search_q else temp_q
        documents = Document.objects.filter(search_q)
        total_count = len(documents)
        total_page = math.ceil(total_count / paginated_by)
        page_range = range(1, total_page + 1)
        start_index = paginated_by * (page - 1)
        end_index = paginated_by * page

        documents = documents[start_index:end_index]

        render(request, 'board/document_list.html',
               {'object_list': documents, 'total_page': total_page, 'page_range': page_range})

        if not documents.exists():
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


    documents = Document.objects.all()

    total_count = len(documents)
    total_page = math.ceil(total_count / paginated_by)
    page_range = range(1, total_page + 1)
    start_index = paginated_by * (page - 1)
    end_index = paginated_by * page

    documents = documents[start_index:end_index]

    current_top_num = len(Document.objects.all()) - paginated_by * (page - 1)

    return render(request, 'board/document_list.html',
                  {'object_list': documents, 'total_page': total_page, 'page_range': page_range, 'currentTopNum':current_top_num})


from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def document_create(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        form.instance.author_id = request.user.id
        if form.is_valid():
            form.save()
            return JsonResponse({'works':True})
        return JsonResponse({'notValid':True})
    else:
        if request.is_ajax():
            if request.user.is_anonymous:
                return JsonResponse({'notLogin':True})
            form = DocumentForm() # empty page
            html = render_to_string('board/document_create.html', {'form':form})
            return JsonResponse({'html':html})
        raise Http404

def document_update(request, document_id):
    if request.method == "POST":

        document = get_object_or_404(Document, pk=document_id)
        form = DocumentForm(request.POST, request.FILES, instance=document)

        if form.is_valid():
            document = form.save()
            return redirect(document)
    else:
        document = get_object_or_404(Document, pk=document_id)
        form = DocumentForm(instance=document)
    return render(request, 'board/document_update.html', {'form':form})

def document_detail(request, document_id):

    document = get_object_or_404(Document, pk=document_id)
    comment_form = CommentForm()
    comments = document.comments.all()
    return render(request, 'board/document_detail.html', {'object':document, 'comments':comments, 'comment_form':comment_form})


from .forms import CommentForm
def comment_create(request, document_id):
    if request.user.is_anonymous:
        return JsonResponse({'notLogin':True})
    if request.is_ajax():
        document = get_object_or_404(Document, pk=document_id)
        comment_form = CommentForm(request.POST)
        comment_form.instance.author_id = request.user.id
        comment_form.instance.document_id = document_id
        if comment_form.is_valid():
            comment = comment_form.save()

        html = render_to_string('board/comment/comment_single.html',{'comment':comment})
        return JsonResponse({'html':html})

    raise Http404


from django.contrib import messages
from .models import Comment
def comment_update(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user != comment.author and not request.user.is_staff:
        return JsonResponse({'notAuthor':True})
    if request.is_ajax():
        form = CommentForm(request.GET, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({'works':True})
        else:
            return JsonResponse({'notValid':True})
    raise Http404

def comment_delete(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    document = Document.objects.get(pk=comment.document.id)
    if request.user != comment.author and not request.user.is_staff:
        print(comment_id)
        messages.warning(request, "권한 없음")
        return redirect(document)

    if request.is_ajax():
        comment.delete()
        return JsonResponse({'works':True})

    if request.method == "POST":
        comment.delete()
        return redirect(document)

    raise Http404


def document_delete(request, document_id):
    if request.is_ajax():
        document = Document.objects.get(pk=document_id)
        if request.user != document.author and not request.user.is_staff:
            return JsonResponse({'notAuthor':True})
        document.delete()
        return JsonResponse({'works':True})
    raise Http404


from django.http import JsonResponse
def get_data_ajax(request):
   data = {
       "name" : "jake",
       "age" : 100,
       "bloodtype" : "o"
   }
   return JsonResponse(data)
