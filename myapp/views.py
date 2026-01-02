from django.shortcuts import render,redirect
from .models import Post
#git
def home (request):
    posts=Post.objects.all() 
    return render (request,'home.html',{'posts':posts})

    




