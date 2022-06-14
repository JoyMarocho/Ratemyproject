from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, ProfileForm,UploadProjectForm,UpdateUserForm,RatingsForm,PostForm
from rest_framework import authentication,permissions,serializers,viewsets
from .models import Project,Profile,Rating,Post
from .serializer import ProfileSerializer,ProjectSerializer,UserSerializer,PostSerializer
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
import json, random

# Create your views here.
def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    else:
        form = PostForm()

    try:
        posts = Post.objects.all()
        posts = posts[::-1]
        a_post = random.randint(0, len(posts)-1)
        random_post = posts[a_post]
        print(random_post.photo)
    except Post.DoesNotExist:
        posts = None
    return render(request, 'index.html', {'posts': posts, 'form': form, 'random_post': random_post})

    # message = "Welcome to Rate-My-Project"
    # return render(request,'index.html',{"message": message})

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    

def register_user(request):
    form = NewUserForm(request.POST)
    if request.method == 'POST' and form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
            messages.error(request, f'Unsuccessful registration. Invalid information.')
            form = NewUserForm()
    return render(request, 'registration/registration_form.html', {'registration_form': form})

        # form = NewUserForm(request.POST)
        # if request.method == "POST" and  form.is_valid():
        #     user = form.save()
        #     login(request, user)
        #     messages.success(request, f'Registration Successful.')
        #     return redirect('homepage')
        # messages.error(request, f'Unsuccessful registration. Invalid information.')
        # form = NewUserForm()
        # return render(request, 'registration/registration_form.html', {"registration_form": form})

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

@login_required(login_url='login')
def profile(request, username):
    # user = User.objects.get()
    # user.save()
    return render(request,'profile/profile.html')

def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    params = {
        'user_prof': user_prof,
    }
    return render(request, 'profile/userprofile.html', params)

@login_required(login_url='login')
#@transaction.atomic
def update_profile(request, username):
    user = User.objects.get(username=username)
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

@login_required(login_url='login')
def project(request, post):
    post = Post.objects.get(title=post)
    ratings = Rating.objects.filter(user=request.user, post=post).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(post=post)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingsForm()
    params = {
        'post': post,
        'rating_form': form,
        'rating_status': rating_status

    }
    return render(request, 'new_project.html', params)



# class ListProjects(APIView):
#     """
#     View to list all users in the system.

#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
#         # authentication_classes = [authentication.TokenAuthentication]
#         # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Project.objects.all()

#     def get(self, request, format=None):
#         all_projects = Project.objects.all()
#         serializers = ProjectSerializer(all_projects, many=True)
#         return Response(serializers.data)

# class ListUserProfile(APIView):
#         # authentication_classes = [authentication.TokenAuthentication]
#         # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Profile.objects.all()

#     def get(self,request, format=None):
#         profile_details = Profile.objects.all()
#         serializers = ProfileSerializer(profile_details, many=True)
#         return Response(serializers.data)

# class ProjectCreateView(LoginRequiredMixin,CreateView):
#         form_class = UploadProjectForm
#         template_name = 'new_project.html'

# def form_valid(self, form):
#         form.instance.username = self.request.user
#         return super().form_valid(form)


class ProjectListView(ListView):
    model = Project
    template_name = 'index.html'


def search_project(request):
    if request.method == 'GET':
        title = request.GET.get("title")
        results = Post.objects.filter(title__icontains=title).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'results.html', {'message': message})
