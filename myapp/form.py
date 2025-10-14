from django import forms 
from .models import Post
class AddForms(forms.ModelForm):
    class Meta():
        model=Post
        field=['title' ,'content']