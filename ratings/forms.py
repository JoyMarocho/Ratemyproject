from django.db.models import fields
from django.forms.models import model_to_dict
from ratings.models import Profile,Project
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Your forms here
class NewUserForm(UserCreationForm):
    email = forms.EmailField()

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

        class Meta:
            model = User
            fields = ['username', 'email']

class ProfileForm(forms.ModelForm):

        class Meta:
            model = Profile
            fields = ('profile_picture','user','bio','location','occupation')

