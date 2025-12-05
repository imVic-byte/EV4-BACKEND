from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

def handler404(request, exception):
    return JsonResponse({
        'error': 'Ruta no encontrada',
        'detail': f'La ruta {request.path} no existe en esta API.',
        'status': 404
    }, status=404)

def handler400(request, exception=None):
    return JsonResponse({
        'error': 'Solicitud incorrecta',
        'detail': 'La solicitud no pudo ser procesada debido a un error del cliente.',
        'status': 400
    }, status=400)

def handler500(request):
    return JsonResponse({
        'error': 'Error interno del servidor',
        'detail': 'Ha ocurrido un error inesperado. Por favor contacte al administrador.',
        'status': 500
    }, status=500)