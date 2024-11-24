from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register({
    Author, BlogCategory, Tag, Blog, Newsletter, Comment, SubComment
})
