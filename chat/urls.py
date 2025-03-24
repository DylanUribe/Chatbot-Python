from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chatbot_view, name='chatbot'), 
    path('get_response/', views.get_response, name='get_response'), 
]