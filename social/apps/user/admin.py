from .models import User
from .forms import SignUpForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Register your models here.


class ManagingUsers(UserAdmin):

	add_form = SignUpForm

	list_display = ['__str__']
	search_fields = ['email']
	readonly_fields = ['date_joined', 'last_login']
	ordering = ('id',)

	filter_horizontal = []
	list_filter = []


	add_fieldsets = (

		('Add a new user', {
			'classes':('wide',),
			'fields': ('first_name', 'last_name' ,'email', 'birthday', 'password1', 'password2', 'avatar', 'cover_pic', 'validated', 'is_admin', 'is_staff', 'is_active', 'is_superuser'),
			}),
		)
	
	fieldsets = (

		(None, {
			'fields': ('first_name', 'last_name', 'bio' ,'email', 'birthday', 'avatar', 'cover_pic', 'is_admin',  'is_staff', 'is_active', 'is_superuser'),
			}),

		)
admin.site.register(User, ManagingUsers)