from django.urls import re_path as url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('posts', views.PostViewSet)
router.register('profile', views.ProfileViewSet)

urlpatterns = [
    url('', views.index, name='index'),
    url('signup/', views.signup, name='signup'),
    url('account/', include('django.contrib.auth.urls')),
    url('api/', include(router.urls)),
    url('<username>/profile', views.user_profile, name='userprofile'),
    url('api-auth/', include('rest_framework.urls', namespace='framework')),
    url('profile/<username>/', views.profile, name='profile'),
    url('profile/<username>/settings', views.edit_profile, name='edit'),
    url('project/<post>', views.project, name='project'),
    url('search/', views.search_project, name='search'),
]

