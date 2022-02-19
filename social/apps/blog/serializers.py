from genericpath import exists
from rest_framework import serializers
from user.serializers import SnippetAuthorSerializer
from .models import Post, Comment, SnippetFile, React

class SharedPostSerializer(serializers.ModelSerializer):
    author = SnippetAuthorSerializer()
    media = serializers.SerializerMethodField(method_name='get_media')

    def get_media(self, snippet):
        return [m.media.url for m in snippet.media.all()]
        
    class Meta:
        model = Post
        fields = ('id', 'author', 'date', 'content', 'media',)

class SnippetSerializer(SharedPostSerializer):
    author = SnippetAuthorSerializer()
    reacts = serializers.SerializerMethodField(method_name='get_reacts_count')
    
    reacted = serializers.SerializerMethodField(method_name='reactant')

    class Meta(SharedPostSerializer.Meta):
        fields = SharedPostSerializer.Meta.fields + ( 'reacts', 'reacted',)

    def get_reacts_count(self, snippet):
        counts = snippet.reacts.count()
        return counts

    def reactant(self, snippet):
        return snippet.reacts.filter(user= self.context.get('user')).exists()

    

class PostSerializer(SnippetSerializer):
    post = SharedPostSerializer()
    comments = serializers.SerializerMethodField(method_name='comments_count')
    shares = serializers.SerializerMethodField(method_name='shares_count')
    
    def comments_count(self, post):
        counts = post.post_comments.count()
        return counts

    def shares_count(self, post):
        counts = post.post_posts.count()
        return counts

    class Meta(SnippetSerializer.Meta):
        model = Post
        fields = SnippetSerializer.Meta.fields + ('post', 'comments', 'shares')

class CommentCreationSerial(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', 'author', 'post')


class PostCreationSerial(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('content', 'author',)

class CommentSerializer(SnippetSerializer):
    class Meta:
        model = Post
        fields = SnippetSerializer.Meta.fields 
