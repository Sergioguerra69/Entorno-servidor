from django.shortcuts import render
import google.generativeai as genai

def chat_view(request):
    #si quieres ocultar la api tendrias que hacelo por .env
    API_KEY = "AIzaSyBVUqv5Y9WYM9UOCYUiMkmB_6KC2EpNAEE"
    
    # Si el usuario quiere ver el chat (GET)
    if request.method == 'GET':
        return render(request, 'chatbot/chat.html')
    
    # si el usuario envio un mensaje (POST)
    if request.method == 'POST':
        # agarro lo que escribió
        pregunta = request.POST.get('prompt', '').strip()
        
        if pregunta:
            try:
                # le pregunto a Gemini
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-2.5-flash')
                respuesta = model.generate_content(pregunta)
                
                # le muestro la respuesta
                return render(request, 'chatbot/chat.html', {
                    'respuesta': respuesta.text,
                    'prompt_usuario': pregunta
                })
                
            except Exception as e: #cualquier error dentro de try
                # algo falló
                return render(request, 'chatbot/chat.html', {
                    'respuesta': f"Error: {str(e)[:100]}",
                    'prompt_usuario': pregunta
                })
    
    # si no hay pregunta, muestro el chat vacío
    return render(request, 'chatbot/chat.html')