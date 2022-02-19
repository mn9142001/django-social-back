from django.db import models
def get_img_path(instance, filename):
	cl = instance.__class__.__name__
	if cl == 'Page':
		final = 'Cover/{0}'.format(filename)
	else:
		final = filename
	return '{0}/{1}/{2}'.format(cl, instance.name, final)

# Create your models here.
class BluePrint(models.Model):
	admin = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='%(class)sAdmin', null=True, blank=True)
	sub_admin = models.ManyToManyField('user.User', related_name='%(class)sSubAdmin', blank=True)
	cover = models.ImageField(upload_to=get_img_path, null=True, blank=True)
	name  = models.TextField()
	members = models.ManyToManyField('user.User', related_name='%(class)sMembers', blank=True)
	blocked = models.ManyToManyField('user.User', related_name='%(class)sBlocked', blank=True)

	class Meta:
		abstract = True

	def __str__(self):
		return self.name

class Group(BluePrint):
	waiting = models.ManyToManyField('user.User', related_name='group_waiting_members', blank=True)


class Page(BluePrint):
	avatar = models.ImageField(upload_to=get_img_path, null=True, blank=True)
	bio   = models.TextField(null=True, blank=True)
	validated = models.BooleanField(default=False)