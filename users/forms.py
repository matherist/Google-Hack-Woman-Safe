from django import forms
from django.forms import widgets
from . models import *
from . forms import *
from django.contrib.auth.forms import UserCreationForm

# class NotesForm(forms.ModelForm):
#     class Meta:
#         model = Notes
#         fields = ['title', 'description']
        
class DateInput(forms.DateInput):
    input_type = 'date'
    


class UserRegistrationForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ["username", "password1", "password2"]



class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ['photo', 'text']