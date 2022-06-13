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

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
            return redirect('homepage')
        else:
            messages.error(request, f'Invalid Username or password')
    else:
            messages.error(request, f'Invalid username or password')
    form = AuthenticationForm()
    return render(request, 'registration/login_form.html', {"login_form": form})


def logout_user(request):
    logout(request)
    messages.info(request, f'You have successfully logged out.')
    return redirect('login')

@login_required
def profile(request):
    # user = User.objects.get()
    # user.save()
    return render(request,'profile/profile.html')


@login_required
#@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profileupdate')
        else:
            messages.error(request,f'Please try updating your profile again.')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request,'profile/update_profile.html',{"profile_form":profile_form, "user_form": user_form, "prolife_form":profile_form})


class ListProjects(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
        # authentication_classes = [authentication.TokenAuthentication]
        # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Project.objects.all()

def get(self,request,format=None):
    all_projects = Project.objects.all()
    serializers = ProjectSerializer(all_projects, many=True)
    return Response(serializers.data)

class ListUserProfile(APIView):
        # authentication_classes = [authentication.TokenAuthentication]
        # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Profile.objects.all()

def get(self,request,format=None):
    profile_details = Profile.objects.all()
    serializers = ProfileSerializer(profile_details, many=True)
    return Response(serializers.data)