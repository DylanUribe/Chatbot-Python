from django.db import models
from django.contrib.auth.models import User


class Pregunta(models.Model):
    texto = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.texto

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.TextField()

    def __str__(self):
        return self.texto

class ChatMessage(models.Model):
    user = models.CharField(max_length=100)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.message[:50]}"

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255, default="Sin título")
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=(('user', 'User'), ('bot', 'Bot')))
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)