from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .serializers import StatusSerializer, ErrorSerializer
from .models import ErrorReport
from django.http import JsonResponse


@api_view(['GET'])
def get_server_status(request):
    # cuando alguien pide saber si el servidor esta activo
    return Response(StatusSerializer(
        {'status': 'running', 'date': datetime.now()}).data)

@api_view(['GET'])
def get_errors(request):
    # cuando alguien pide todos los errores guardados
    errors = ErrorReport.objects.all()
    return Response(ErrorSerializer(errors, many=True).data)

@api_view(['GET'])
def get_error_from_code(request, code):
    # cuando alguien pide un error en especifico
    try:
        error = ErrorReport.objects.get(code=code)
        return Response(ErrorSerializer(error).data)
    except ErrorReport.DoesNotExist:
        # si no existe ese codigo de error
        return Response(
            {'error': 'Error report not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
def create_error(request):
    # cuando quieres guardar un error nuevo
    serialized_error = ErrorSerializer(data=request.data)# traduce JSON a python
    if serialized_error.is_valid():
        serialized_error.save()
        #el servidor responde al cliente
        return Response(serialized_error.data, status=status.HTTP_201_CREATED) 
    return Response(serialized_error.errors, status=status.HTTP_400_BAD_REQUEST)#cuando haces un error mal

# actualizar o eliminar
@api_view(['PUT', 'DELETE'])
def error_update(request, id):
    # buscar el error por su id
    try:
        error_obj = ErrorReport.objects.get(id=id)
    except ErrorReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # PUT = ACTUALIZAR
    if request.method == 'PUT':
        serialized_data = ErrorSerializer(error_obj, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)#saca el JSON del serializer
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE = BORRAR
    if request.method == 'DELETE':
        error_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)