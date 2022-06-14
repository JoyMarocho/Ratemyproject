from django.contrib import admin
from .models import Project, Rating,Profile,Post


# Register your models here.
admin.site.register(Project)
admin.site.register(Rating)
admin.site.register(Profile)
admin.site.register(Post)
