from django.urls import re_path as url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('posts', views.PostViewSet)
router.register('profile', views.ProfileViewSet)

urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(), name='homepage'),
    url(r'register', views.register_user, name='register'),
    url(r'login', views.login_user, name='login'),
    url(r'logout', views.logout_user, name='logout'),
    url(r'api/', include(router.urls)),
    url('project/<post>', views.project, name='project'),
    url('search/', views.search_project, name='search'),
    # url(r'new/project/$', views.ProjectCreateView.as_view(), name='project_add'),
    #url(r'^profile/(?P<user_id>\d+)', views.profile, name='profiles'),
    url(r'profile/', views.profile, name='profileupdate'),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'update_profile', views.update_profile, name='update_profile'),
    # url(r'^api/project/$', views.ListProjects.as_view()),
    # url(r'^api/profile/$', views.ListUserProfile.as_view()),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)