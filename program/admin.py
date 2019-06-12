from django.contrib import admin

from .models import Category, Program, Schedule, Comment
# Register your models here.

class CommentOption(admin.ModelAdmin):
    list_display = ['nickname', 'text']

class CommentInline(admin.TabularInline):
    model = Comment

class CategoryOption(admin.ModelAdmin):
    list_display = ['name', 'period', 'place']
    inlines = [CommentInline]

class ScheduleOption(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'time']

admin.site.register(Category, CategoryOption)
admin.site.register(Program)
admin.site.register(Schedule, ScheduleOption)
admin.site.register(Comment, CommentOption)