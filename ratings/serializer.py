from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Post

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ('user','bio','profile_picture')

        def get_profile_picture(self,obj):
            if obj.profile_picture:
                return obj.profile_picture
            return 'https://www.wallpaperflare.com/boruto-digital-wallpaper-uzumaki-boruto-jogan-one-person-real-people-wallpaper-hxetu'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'description', 'technologies', 'photo', 'date', 'user']



class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'profile', 'posts']