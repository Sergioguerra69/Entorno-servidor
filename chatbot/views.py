from django.shortcuts import render
import google.generativeai as genai

def chat_view(request):
    API_KEY = "AIzaSyBVUqv5Y9WYM9UOCYUiMkmB_6KC2EpNAEE"
    
    if request.method == 'POST':
        pregunta = request.POST.get('prompt', '').strip()
        
        if pregunta:
            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-2.5-flash')
                respuesta = model.generate_content(pregunta)
                
                return render(request, 'chatbot/chat.html', {
                    'respuesta': respuesta.text,
                    'prompt_usuario': pregunta
                })
                
            except Exception as e:
                error_msg = str(e)
                return render(request, 'chatbot/chat.html', {
                    'respuesta': f"Error: {error_msg[:100]}",
                    'prompt_usuario': pregunta
                })
    
    return render(request, 'chatbot/chat.html')