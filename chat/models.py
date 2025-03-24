from django.db import models

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

