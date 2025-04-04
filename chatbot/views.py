from django.http import JsonResponse
from django.shortcuts import render
from .functions import get_python_response  
from .models import Conversation


def chatbot_view(request):
    return render(request, "chatbot/chatbot.html")

def get_response(request):
    message = request.GET.get("message", "")  
    response_text = get_python_response(message)  
    return JsonResponse({"response": response_text})

def chat_page(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chat_page.html', {
        'conversations': conversations
    })