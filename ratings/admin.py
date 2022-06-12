from django.contrib import admin
from .models import Project, Rating,Profile


# Register your models here.
admin.site.register(Project)
admin.site.register(Rating)
admin.site.register(Profile)