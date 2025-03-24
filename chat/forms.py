from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ChatMessage
from django.contrib.auth import get_user_model


User = get_user_model()  # Obtiene el modelo de usuario actual

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingrese una dirección de correo válida.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]  # Asegúrate de incluir el email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ["user", "message", "response"]