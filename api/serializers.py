from rest_framework import serializers
from .models import ErrorReport
#para cuando el servidor dice si esta todo bien
class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=100)
    date = serializers.DateTimeField()
#cuando alguien reporta un error
class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReport
        fields = ['id', 'code', 'description', 'date']
        
     