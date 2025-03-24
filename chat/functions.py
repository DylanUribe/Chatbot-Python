import requests
import json

def get_python_response(message):
    url = "http://127.0.0.1:11434/api/chat"  # Endpoint correcto
    payload = {
        "model": "llama2:latest",  # Asegurar que el modelo está bien definido
        "messages": [{"role": "user", "content": message}]
    }
    headers = {
        "Content-Type": "application/json"  # Encabezado necesario
    }

    try:
        response = requests.post(url, json=payload, headers=headers, stream=True)  # Streaming activado
        response.raise_for_status()

        full_response = ""  # Acumulador para juntar el mensaje completo

        # Leer línea por línea del stream
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode("utf-8"))  # Decodificar línea JSON
                    if "message" in json_data and "content" in json_data["message"]:
                        full_response += json_data["message"]["content"]  # Concatenar texto
                except json.JSONDecodeError as e:
                    print("Error decodificando JSON:", e)  # Depuración

        return full_response.strip() if full_response else "Lo siento, no entendí tu pregunta."
    
    except requests.exceptions.RequestException as e:
        return f"Hubo un error al obtener la respuesta: {str(e)}"
