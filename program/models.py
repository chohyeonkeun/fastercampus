from django.db import models

from django.contrib.auth import get_user_model
# Create your models here.
from django.urls import reverse
class Category(models.Model):
    name = models.CharField(max_length=50)  # R 데이터 분석
    description = models.TextField()  # R을 활용하여 입문자도 쉽게 데이터 분석의 기초부터 실전까지 제대로 배워보세요!
    # period = models.CharField(max_length=100)  # 19.06.01~19.08.31
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True) # 19-06-01-%H-%M-%S
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True) # 19-08-01-%H-%M-%S
    place = models.CharField(max_length=50)  # 2호선 성수역 부근 패스트캠퍼스 강의장
    image = models.ImageField(upload_to='program_photo/%Y/%m/%d', default=True)
    detail_title = models.CharField(max_length=50, default=True) # 비전공자도 1년차 실력과 경험을 갖춘 데이터 사이언티스트로.
    detail_text = models.TextField(default=True) # 데이터 사이언스 SCHOOL FIT은 성공적인~~.
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category:detail', args=[self.id])

class Program(models.Model):
    name = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="program_name")  # R 데이터 분석
    # time = models.CharField(max_length=100)  # 19:00 ~ 24:00
    start_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True) # 19:00:00
    end_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True) # 24:00:00
    # slug = models.SlugField(max_length=120, db_index=True, unique=True, allow_unicode=True, blank=True)
    teacher = models.CharField(max_length=20)  # 박지웅
    place = models.CharField(max_length=50)  # 2호선 성수역 부근 패스캠퍼스 B강의장
    enroll = models.ManyToManyField(get_user_model(), related_name="enrolled_program", blank=True)

    def __str__(self):
        return self.teacher
    

class Schedule(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default="", related_name="schedule_user")
    name = models.CharField(max_length=50)
    teacher = models.CharField(max_length=20)
    start_time = models.TimeField(auto_now_add=False, blank=True, null=True)
    end_time = models.TimeField(auto_now=False, blank=True, null=True)

class Comment(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="comment_category", default="")
    nickname = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="comment_nickname")
    text = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text
