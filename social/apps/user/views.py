from multiprocessing import context
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, SnippetAuthorSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from user.models import User
from .serializers import UserProfileSerializer, UserCreation
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def UnFollowParties(requester, user):
    if requester in user.following.all():
        user.following.remove(requester)
    if user in requester.followers.all():
        requester.followers.remove(user)
    user.save()

class UserProfile(ViewSet):
    def create(self, request):
        pk = request.data.get('userID')
        user = get_object_or_404(User, pk=pk)
        if user in request.user.following.all():
            UnFollowParties(request.user, user)
        else:
            request.user.following.add(user)
        return Response(True)

    def retrieve(self, request, pk):
        return Response(UserProfileSerializer(User.objects.get(pk=pk), context={'visitor':request.user}).data)

class UserView(ViewSet):
    permission_classes = ()
    authentication_classes = ()
    def create(self, request):
        serial = UserCreation(data=request.data)
        if serial.is_valid():
            res = {}
            user = serial.save()
            token = RefreshToken.for_user(user)
            res['access'] = str(token.access_token)
            res['refresh'] = str(token)
            res['user'] = SnippetAuthorSerializer(user).data

            return Response(res)

        return Response({'error': serial.errors})