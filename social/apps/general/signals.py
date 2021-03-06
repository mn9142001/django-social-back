from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Notifications
from blog.models import Post, Comment, React
from blog.models import React
from .serializers import NotificationsSerializer
channel_layer = get_channel_layer()
			#async_to_sync(channel_layer.group_send)('chat_{0}_with_{1}'.format(partner.id, request.user.id),{'type' : 'chat_message' , 'message' : message, 'other' : request.user.id})

@receiver(post_save, sender=Notifications)
def NotificationsSignal(sender, instance, **kwargs):
    notify_group_name = 'general_%d'% instance.receiver.pk
    async_to_sync(channel_layer.group_send)(
        notify_group_name, {'type': 'chat_message', 'notify': NotificationsSerializer(instance).data})

# @receiver(post_delete, sender=Notifications)
# def DeleteNotificationsSignal(sender, instance, **kwargs):
#     print("working")
    
# @receiver(post_save, sender=Comment)
# def AfterComment(sender, instance, **kwargs):
#     pass

# @receiver(post_save, sender=React)
# def AfterReact(sender, instance, **kwargs):
#     pass