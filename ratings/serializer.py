from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project,Profile


class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ('title','image','description','link')


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ('user','bio','profile_picture')

        def get_profile_picture(self,obj):
            if obj.profile_picture:
                return obj.profile_picture
            return 'https://www.wallpaperflare.com/boruto-digital-wallpaper-uzumaki-boruto-jogan-one-person-real-people-wallpaper-hxetu'