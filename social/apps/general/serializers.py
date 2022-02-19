from rest_framework import serializers
from .models import Notifications
from user.serializers import SnippetAuthorSerializer
class NotificationsSerializer(serializers.ModelSerializer):
    sender = SnippetAuthorSerializer()
    class Meta:
        model = Notifications
        fields = ('id', 'sender', '_context')
