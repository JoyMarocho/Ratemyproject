from django.urls import re_path as url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(), name='homepage'),
    url(r'register', views.register_user, name='register'),
    url(r'login', views.login_user, name='login'),
    url(r'logout', views.logout_user, name='logout'),
    url(r'new/project/$', views.ProjectCreateView.as_view(), name='project_add'),
    #url(r'^profile/(?P<user_id>\d+)', views.profile, name='profiles'),
    url(r'profile/', views.profile, name='profileupdate'),
    url(r'update_profile', views.update_profile, name='update_profile'),
    url(r'^api/project/$', views.ListProjects.as_view()),
    url(r'^api/profile/$', views.ListUserProfile.as_view()),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)