"""front URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from rest_framework import routers
from core.views import MemberViewSet, EventViewSet, view_log_events, OlaMundoView
from django.urls import include

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'events', EventViewSet)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('ver_logs/', view_log_events, name='ver_logs'),

    path('ola_mundo/', OlaMundoView.as_view(), name='ola_mundo'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
