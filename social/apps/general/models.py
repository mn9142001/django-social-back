from django.db import models

# Create your models here.
class Notifications(models.Model):
	_types = ((1,'react'), (2, 'follow'))
	sender = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user_created_notifies')
	receiver = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user_received_notifies')
	seen = models.BooleanField(default=False)
	_context = models.IntegerField(choices=_types)
	post = models.ForeignKey('blog.Post', null=True, on_delete=models.CASCADE)
	comment = models.ForeignKey('blog.Comment', null=True, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)