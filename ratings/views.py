from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewUserForm, ProfileForm,UploadProjectForm,UpdateUserForm
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer
from .models import Project,Profile
from rest_framework import authentication, permissions, serializers
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
def index(request):
    message = "Welcome to Rate-My-Project"
    return render(request,'index.html',{"message": message})


def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Registration Successful.')
        return redirect('homepage')
    messages.error(request, f'Unsuccessful registration. Invalid information.')
    form = NewUserForm()
    return render(request, 'registration/registration_form.html', {"registration_form": form})
