from django.contrib import admin

from .models import Category, Program, Comment
# Register your models here.

class CommentOption(admin.ModelAdmin):
    list_display = ['nickname', 'text']

class CommentInline(admin.TabularInline):
    model = Comment

class CategoryOption(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'place']
    prepopulated_fields = {'slug':('name',)}
    inlines = [CommentInline]

class ProgramOption(admin.ModelAdmin):
    list_display = ['name', 'teacher']
    prepopulated_fields = {'slug':('teacher',)}


admin.site.register(Category, CategoryOption)
admin.site.register(Program, ProgramOption)
admin.site.register(Comment, CommentOption)