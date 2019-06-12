from django.db import models
from django.urls import reverse
# Create your models here.
'''
2. 모델 document - author, cartegory,title, text, image, created, updated
3. 모델 category - slug, name
'''
class Board(models.Model):
    pass
class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=30, db_index=True, unique=True, allow_unicode=True)
    description = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name

from django.contrib.auth import get_user_model
class Document(models.Model):

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, db_index=True, unique=True, allow_unicode=True)
    text = models.TextField()
    image = models.ImageField(upload_to='board_images/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("board:detail", args=[self.id])

class Comment(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')

    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return (self.author.username if self.author else "무명") + "의 댓글"

    class Meta:
        ordering = ['-id']

