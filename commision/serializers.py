from rest_framework import serializers

from .models import Device, Command, Category

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['name', 'id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'id']
        
class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = '__all__'
        
