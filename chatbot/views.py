import os
from django.http import JsonResponse
from django.shortcuts import render
from openai import OpenAI
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

class ChatbotGenerateAnswerView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'chatbot/chatbot.html'

    def get(self, request):
        return render(request, 'chatbot/chatbot.html')

    def _generate_response(self, prompt):
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        completions = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        response = completions.choices[0].message.content
        return response

    def post(self, request):
        message = request.data['message']
        response = self._generate_response(message)
        return JsonResponse({'response': response})

# Ajoutez cette vue si nécessaire
def chatbot_view(request):
    return render(request, 'chatbot/chatbot.html')