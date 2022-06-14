from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ratings.models import Profile,Project,Rating
from django.db.models import fields
from django.forms.models import model_to_dict
from django.forms import ImageField

#Your forms here
class NewUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self,commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UpdateUserForm(forms.ModelForm):
        email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

        class Meta:
            model = User
            fields = ['username', 'email']

class ProfileForm(forms.ModelForm):

        class Meta:
            model = Profile
            fields = ('name','profile_picture','user','bio','location','occupation')

class UploadProjectForm(forms.ModelForm):

        class Meta:
            model = Project
            fields = ('title','image','description','link','rating')

class RatingsForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['design', 'usability', 'content']