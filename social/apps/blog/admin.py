from asyncio import constants
from django.contrib import admin
from .models import Post, Comment, React, SnippetFile
# Register your models here.
admin.site.register([Post, Comment, React, SnippetFile])

