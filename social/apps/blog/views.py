from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Post, Comment, React, SnippetFile
from .serializers import PostSerializer, PostCreationSerial, CommentCreationSerial, CommentSerializer
from rest_framework.decorators import api_view
from .decorators import SnippetDecorator

class PostViewSet(ViewSet):

	def create(self, request):
		serial = PostCreationSerial(data=request.data)
		if serial.is_valid():
			if request.data.get('postID'):
				_post = Post.objects.get(pk=request.data.get('postID'))
				if _post.post:
					_post = _post.post
				post = serial.save(author=request.user, post=_post)
			else:
				post = serial.save(author=request.user)

			if request.data.get('media') and int(request.data.get('media')) > 0:
				for x in range(int(request.data.get('media'))):
					file = SnippetFile.objects.create(media=request.data.get('img_' + str(x)))
					post.media.add(file)
			
			return Response({'post': PostSerializer(post, context={'user': request.user}).data})
		return Response(serial.errors)

	def list(self, request):
		queryset = Post.objects.all()[:10]
		return Response({'posts': PostSerializer(queryset, context={'user': request.user}, many=True).data})

	def retrieve(self, request, pk):
		length = int(pk)
		queryset = Post.objects.all()[length:][:length + 5]
		if any(queryset):
			return Response({'posts': PostSerializer(queryset, context={'user': request.user}, many=True).data})
		return Response(False)

class CommentViewSet(ViewSet):

	def create(self, request):
		serial = CommentCreationSerial(data=request.data)
		if serial.is_valid():
			respo = {}
			try:
				post =Post.objects.get(pk=request.data.get('postID'))
				comment = serial.save(author=request.user, post=post)
				respo['counts'] = post.post_comments.all().count()
			except:
				_comment =Comment.objects.get(pk=request.data.get('commentID'))
				comment = serial.save(author=request.user, drag=_comment)

			if request.data.get('media'):
				file = SnippetFile.objects.create(media=request.data.get('media'))
				comment.media.add(file)
			respo['comment'] = CommentSerializer(comment, context={'user': request.user}).data
			return Response(respo)
		return Response(serial.errors)

	def retrieve(self, request, pk):
		post = Post.objects.get(pk=pk)
		comments = post.post_comments.all().order_by('-id')[:10]
		return Response({'comments': CommentSerializer(comments, context={'user': request.user}, many=True).data})


class ReplyViewSet(ViewSet):
	def retrieve(self, request, pk):
		comment = Comment.objects.get(pk=pk)
		comments = comment.comment_replies.all()[:10]
		return Response({'comments': CommentSerializer(comments, context={'user': request.user}, many=True).data})



@api_view(['post'])
@SnippetDecorator
def SnippetReact(request, snippet=None):
	reacts = React.objects.create(user=request.user, react=request.data.get('_react'))
	snippet.reacts.add(reacts)
	return Response({'counts' :snippet.reacts.count() , 'react': True})