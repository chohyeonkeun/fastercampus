from django.contrib import admin
from .models import Category, Document, Comment

# Register your models here.
class CategoryOption(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    # slug 옵션
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryOption)

class CommentInLine(admin.TabularInline):
    model = Comment

class DocumentOption(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'slug', 'created', 'updated']
    prepopulated_fields = {'slug':('title',)}
    inline = [CommentInLine]

admin.site.register(Document, DocumentOption)

admin.site.register(Comment)