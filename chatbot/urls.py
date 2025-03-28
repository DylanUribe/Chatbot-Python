"""
URL configuration for chatbot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from chat.views import chatbot_view, get_response  
from django.contrib import admin

urlpatterns = [
    path('', chatbot_view, name='chatbot_view'),
    path("get_response/", get_response, name="get_response"),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('auth/', include('chat.auth_urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
