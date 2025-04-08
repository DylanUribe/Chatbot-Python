from django.urls import path
from . import views
from .views import register_view, login_view, logout_view, chat_list, chat_create, chat_update, chat_delete, ChatMessageListCreate, ChatMessageDetail
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path("", views.login_view, name="login"),
    path('get_response/', views.get_response, name='get_response'), 
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path("chats/", chat_list, name="chat_list"),
    path("chats/new/", chat_create, name="chat_create"),
    path("chats/edit/<int:pk>/", chat_update, name="chat_update"),
    path("chats/delete/<int:pk>/", chat_delete, name="chat_delete"),
    path("api/chats/", ChatMessageListCreate.as_view(), name="api_chat_list"),
    path("api/chats/<int:pk>/", ChatMessageDetail.as_view(), name="api_chat_detail"),
    path('conversations/<int:conversation_id>/download/', views.download_conversation_pdf, name='download_conversation_pdf'),
    path("chats/nueva/", views.start_new_conversation, name="new_conversation"),
]