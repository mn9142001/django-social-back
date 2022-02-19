from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
	gender_type = ((1, 'Male'), (2, 'Female'))
	first_name = forms.CharField(label='First name', max_length=100)
	last_name = forms.CharField(label='last name', max_length=100)
	email = forms.CharField(max_length=255, required=True, widget=forms.EmailInput())
	password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', required=True, widget=forms.PasswordInput)
	birthday = forms.DateField(label='BirthDay', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
	gender = forms.ChoiceField(label='Gender' , choices=gender_type  , widget=forms.RadioSelect)

	class Meta:
		model=User
		fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'gender', )

	def save(self):
		self.instance.name = str(self.cleaned_data['first_name'].capitalize() + " " + self.cleaned_data['last_name'])
		return super().save()
