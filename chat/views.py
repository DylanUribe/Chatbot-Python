from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .functions import get_python_response  
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ChatMessageForm
from .models import ChatMessage
from rest_framework import generics
from .serializers import ChatMessageSerializer
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Conversation, Message
from django.utils import timezone


def chatbot_view(request):
    conversations = []
    if request.user.is_authenticated:
        conversations = Conversation.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "chatbot/chatbot.html", {"conversations": conversations})
 

def get_response(request):
    message = request.GET.get("message", "")  
    response_text = get_python_response(message)  

    # NUEVO: Guardar conversación y mensajes
    if request.user.is_authenticated:
        conversation_id = request.session.get('conversation_id')
        conversation = None

        if conversation_id:
            conversation = Conversation.objects.filter(id=conversation_id, user=request.user).first()

        if not conversation:
            conversation = Conversation.objects.create(
                user=request.user,
                title=f"Conversación de {timezone.now().strftime('%d/%m/%Y %H:%M')}"
            )
            request.session['conversation_id'] = conversation.id

        # Guardar el mensaje del usuario
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=message
        )

        # Guardar la respuesta del bot
        Message.objects.create(
            conversation=conversation,
            role='bot',
            content=response_text
        )

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

def download_conversation_pdf(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{conversation.title}.pdf"'

    p = canvas.Canvas(response)
    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, y, f"Conversación: {conversation.title}")
    y -= 40

    p.setFont("Helvetica", 12)
    for msg in conversation.messages.all().order_by("timestamp"):
        if y < 50:
            p.showPage()
            y = 800
        p.drawString(50, y, f"[{msg.role}] {msg.content}")
        y -= 20

    p.save()
    return response

def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get("message")

        # 1. Obtener o crear una conversación activa para el usuario
        conversation_id = request.session.get('conversation_id')
        conversation = None

        if conversation_id:
            conversation = Conversation.objects.filter(id=conversation_id, user=request.user).first()

        if not conversation:
            conversation = Conversation.objects.create(
                user=request.user,
                title=f"Conversación de {timezone.now().strftime('%d/%m/%Y %H:%M')}"
            )
            request.session['conversation_id'] = conversation.id

        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_input
        )

        response = get_ollama_response(user_input)  

        Message.objects.create(
            conversation=conversation,
            role='bot',
            content=response
        )

        return JsonResponse({'response': response})