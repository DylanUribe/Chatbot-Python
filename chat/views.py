from django.http import JsonResponse
from django.shortcuts import render
from .functions import get_python_response  

def chatbot_view(request):
    return render(request, "chatbot/chatbot.html")  

def get_response(request):
    message = request.GET.get("message", "")  
    response_text = get_python_response(message)  
    return JsonResponse({"response": response_text})
