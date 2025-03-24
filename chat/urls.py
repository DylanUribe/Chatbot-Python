from django.urls import path
from . import views
from .views import register_view, login_view, logout_view, chat_list, chat_create, chat_update, chat_delete, ChatMessageListCreate, ChatMessageDetail



urlpatterns = [
    path("", views.chatbot_view, name="chatbot_view"),
    path('get_response/', views.get_response, name='get_response'), 
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("chats/", chat_list, name="chat_list"),
    path("chats/new/", chat_create, name="chat_create"),
    path("chats/edit/<int:pk>/", chat_update, name="chat_update"),
    path("chats/delete/<int:pk>/", chat_delete, name="chat_delete"),
    path("api/chats/", ChatMessageListCreate.as_view(), name="api_chat_list"),
    path("api/chats/<int:pk>/", ChatMessageDetail.as_view(), name="api_chat_detail"),
]