"""olloc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from myapp import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')
router.register(r'search', views.SearchViewSet, basename='search')
router.register(r'auth', views.Auth, basename='auth')
router.register(r'posts', views.PostView, basename='posts')
router.register(r'comment', views.Comment, basename='comment')
router.register(r'follow', views.FollowViewSet, basename='follow')
router.register(r'timeline', views.Timeline, basename='timeline')
router.register(r'like', views.LikeSet, basename='like')
router.register(r'post-nearby', views.PostNearby, basename='post-nearby')


schema_view = get_schema_view(
   openapi.Info(
      title="OLLOC API",
      default_version='v1',
      description="OLLOC API입니다!!",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="olseconds@kr3.kr"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
