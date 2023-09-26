from rest_framework import serializers

from .models import Device, Command, Category, Vendor

class DeviceSerializer(serializers.ModelSerializer):
    vendor = serializers.SlugRelatedField(queryset=Vendor.objects.all(),slug_field='name')
    class Meta:
        model = Device
        fields = ['vendor', 'name', 'id']


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'id']
        
class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = '__all__'
        
