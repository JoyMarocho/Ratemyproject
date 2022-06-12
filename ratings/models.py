from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from PIL import Image


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=70)
    image = CloudinaryField('image', default='photo.jpeg')
    description = models.TextField(default='project description here')
    link = models.URLField(max_length=300, default='https://appname.herokuapp.com/')
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.ForeignKey('Rating',on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save_project(self):
        self.save()


    def delete_project(self):
        self.delete()

    def get_absolute_url(self):
        return reverse('homepage')

class Rating(models.Model):
    design = models.IntegerField(default=0)
    usability = models.IntegerField(default=0)
    content = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)