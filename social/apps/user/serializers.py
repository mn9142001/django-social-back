from django.dispatch import receiver
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from general.models import Notifications


class UserBluePrintSerializers(serializers.ModelSerializer):
	name = serializers.SerializerMethodField(method_name='get_name')
	avatar = serializers.SerializerMethodField(method_name='get_avatar')

	class Meta:
		abstract = True
		model = User
		fields = ('id', 'name', 'avatar')

	def get_name(self, user):
		return user.full_name()

	def get_avatar(self, user):
		return user.pic()


class SnippetAuthorSerializer(UserBluePrintSerializers):
	pass


class UserCreation(serializers.ModelSerializer):
	password = serializers.CharField(
		write_only=True,
		required=True,
		style={'input_type': 'password', 'placeholder': 'Password'}
	)

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'birthday', 'password')

	def create(self, validated_data):
		validated_data['password'] = make_password(validated_data.get('password'))
		return super().create(validated_data)


class UserProfileSerializer(UserBluePrintSerializers):
	posts = serializers.SerializerMethodField(method_name='get_posts')
	following = serializers.SerializerMethodField(
		method_name='is_visitor_following')
	follower = serializers.SerializerMethodField(method_name='is_user_following')

	def is_visitor_following(self, user):
		visitor = self.context.get('visitor')
		return user in visitor.following.all()

	def is_user_following(self, user):
		visitor = self.context.get('visitor')
		return visitor in user.following.all()

	def get_posts(self, user):
		posts = user.post_author.all()[:10]
		from blog.serializers import PostSerializer
		return PostSerializer(posts, many=True).data

	class Meta(UserBluePrintSerializers.Meta):
		fields = UserBluePrintSerializers.Meta.fields + \
			('cover', 'bio', 'posts', 'following', 'follower')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs):
		from general.serializers import NotificationsSerializer
		data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
		data.update({'user': SnippetAuthorSerializer(self.user).data, 'notifies' : NotificationsSerializer(Notifications.objects.filter(receiver=self.user), many=True).data})
		return data