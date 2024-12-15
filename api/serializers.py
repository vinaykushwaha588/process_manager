from rest_framework import serializers
from .models import System, Process



class SystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = System
        fields = '__all__'

class ProcessSerializer(serializers.ModelSerializer):
    system = SystemSerializer()
    class Meta:
        model = Process
        fields = '__all__'