from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings

def get_profile_pic_path(instance, filename):
	return 'profiles/{0}/pic/{1}'.format(instance.email, filename)


class UserManager(BaseUserManager):

	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):

		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		if password:
			user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.is_active = True

		user.save(using=self._db)
		return user

class User(AbstractBaseUser, PermissionsMixin):

	gender_type = ((1, 'Male'), (2, 'Female'))
	email = models.EmailField(
		('email address'), unique=True, null=True, blank=False)
	first_name = models.CharField(
		('first name'), max_length=15, blank=True, null=True)
	last_name = models.CharField(
		('last name'), max_length=15, blank=True, null=True)
	date_joined = models.DateTimeField(
		('date joined'), auto_now_add=True, blank=True, null=True)
	is_active = models.BooleanField(('active'), blank=True, null=True, default=True)
	is_online = models.BooleanField(('online'), default=True)
	birthday = models.DateField(auto_now_add=False, blank=True, null=True)
	gender = models.IntegerField(choices=gender_type, null=True)
	bio = models.CharField(max_length=100, blank=True, null=True)
	avatar = models.ImageField(
		upload_to=get_profile_pic_path, null=True, blank=True,)
	following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_following')
	followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_followers')
	blocked =models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_blocked')
	validated = models.BooleanField(default=False)

	cover_pic = models.ImageField(
		upload_to=get_profile_pic_path, null=True, blank=True,)
	is_superuser = models.BooleanField(('superuser'), default=False)
	is_admin = models.BooleanField(('admin'), default=False)
	is_staff = models.BooleanField(('staff'), default=False)
	chatted_with = models.ManyToManyField('self', blank=True)
	stranger_chats = models.ManyToManyField('self', blank=True)
	objects = UserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELD = []

	def pic(self):
		if not self.avatar:
			return '/media/profiles/avatar.jpg'
		return self.avatar

	def cover(self):
		if not self.cover_pic:
			return '/media/profiles/cover.png'
		return self.cover_pic

	def full_name(self):
		if not self.first_name:
			return self.email.split('@')[0]
		return self.first_name.capitalize() + " " + self.last_name.capitalize()

	def get_first_name(self):
		if not self.first_name:
			return self.full_name()
		return self.first_name.capitalize()

	
	def __str__(self):
		return str(self.id) + ": " + self.full_name()
