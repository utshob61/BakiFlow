from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.businesses.mixins import TenantMixin
from .services.chatbot import process_bot_query

class ChatbotAskView(TenantMixin, APIView):
    """
    API Endpoint for the BakiFlow AI Assistant.
    """
    def post(self, request, *args, **kwargs):
        query = request.data.get('query')
        if not query:
            return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            business = self.get_business()
            bot_response = process_bot_query(business, query)
            return Response({"response": bot_response})
        except Exception as e:
            return Response({"response": "I'm having a bit of trouble thinking right now. Please try again in a moment."}, status=status.HTTP_200_OK)
