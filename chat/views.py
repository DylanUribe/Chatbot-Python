from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .functions import get_python_response  
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ChatMessageForm
from .models import ChatMessage
from rest_framework import generics
from .serializers import ChatMessageSerializer


def chatbot_view(request):
    return render(request, "chatbot/chatbot.html")  

def get_response(request):
    message = request.GET.get("message", "")  
    response_text = get_python_response(message)  
    return JsonResponse({"response": response_text})

# Registro de usuario
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")  
    else:
        form = CustomUserCreationForm()
    return render(request, "chat/register.html", {"form": form})

# Login de usuario
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")  
    else:
        form = AuthenticationForm()
    return render(request, "chat/login.html", {"form": form})

# Logout de usuario
def logout_view(request):
    logout(request)
    return redirect("/")

# para guardar chat
def chat_list(request):
    chats = ChatMessage.objects.all()
    return render(request, "chat/chat_list.html", {"chats": chats})

def chat_create(request):
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("chat_list")
    else:
        form = ChatMessageForm()
    return render(request, "chat/chat_form.html", {"form": form})

def chat_update(request, pk):
    chat = get_object_or_404(ChatMessage, pk=pk)
    if request.method == "POST":
        form = ChatMessageForm(request.POST, instance=chat)
        if form.is_valid():
            form.save()
            return redirect("chat_list")
    else:
        form = ChatMessageForm(instance=chat)
    return render(request, "chat/chat_form.html", {"form": form})

def chat_delete(request, pk):
    chat = get_object_or_404(ChatMessage, pk=pk)
    if request.method == "POST":
        chat.delete()
        return redirect("chat_list")
    return render(request, "chat/chat_confirm_delete.html", {"chat": chat})

class ChatMessageListCreate(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

class ChatMessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
