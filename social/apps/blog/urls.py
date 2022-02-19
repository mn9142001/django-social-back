from unicodedata import name
from rest_framework import routers
from django.urls import path
from blog.views import PostViewSet, CommentViewSet, SnippetReact, ReplyViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')
router.register('replies', ReplyViewSet, basename='replies')

urlpatterns = [
    path('snippet/react/', SnippetReact, name='snippet-react'),

] + router.urls