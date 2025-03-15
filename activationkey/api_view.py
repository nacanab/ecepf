# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ActivatedDevice


class ValidateActivationKeyView(APIView):
    def post(self, request):
        serial_number = request.data.get('serial_number')

        if not serial_number:
            return Response({"error": "serial_number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = ActivatedDevice.objects.get(serial_number=serial_number, is_active=True)
            return Response({"is_active": True}, status=status.HTTP_200_OK)
        except ActivatedDevice.DoesNotExist:
            return Response({"is_active": False}, status=status.HTTP_200_OK)
        except Exception as e:
            # Gestion des autres erreurs (par exemple, erreur de base de données)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ActivateDeviceView(APIView):
    def post(self, request):
        serial_number = request.data.get('serial_number')
        activation_key = request.data.get('activation_key')

        try:
            device = ActivatedDevice.objects.get(activation_key=activation_key, is_active=False)
            device.serial_number = serial_number
            device.is_active = True
            device.save()
            return Response({"valid": True, "message": "Appareil activé"}, status=status.HTTP_200_OK)
        except ActivatedDevice.DoesNotExist:
            return Response({"valid": False, "message": "Clé d'activation invalide"}, status=status.HTTP_400_BAD_REQUEST)