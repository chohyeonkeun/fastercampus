from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'category'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('list/', Categorylist.as_view(), name='list'),
    path('detail/<int:pk>', CategoryDetail.as_view(), name='detail'),
    path('create/', CategoryCreate.as_view(), name='create'),
    path('delete/<int:pk>', Categorylist.as_view(), name='delete'),
    path('update/<int:pk>', Categorylist.as_view(), name='update'),
    path('comment/create/<int:category_id>', comment_create, name='comment_create'),
    path('comment/update/<int:comment_id>', comment_update, name='comment_update'),
    path('comment/delete/<int:comment_id>', comment_delete, name='comment_delete'),
    path('program/list/', program_list, name='program_list'),
    path('program/submit/', program_submit, name='program_submit'),
    path('mypage/', my_page, name='my_page'),
    path('enroll/delete/', enroll_delete, name='enroll_delete'),
]