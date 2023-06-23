from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import DeviceSerializer, CategorySerializer, CommandSerializer
from .models import Device, Category, Command

class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows devices to be viewed or edited.
    """
    queryset = Device.objects.all().order_by('id')
    serializer_class = DeviceSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categoryes to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

class CommandViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows commands to be viewed or edited.
    """
    queryset = Command.objects.all().order_by('id')
    serializer_class = CommandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['for_device']
    

def commision_view(request):
    templane_name = 'templates/commision/commision.html'
    return render(request, templane_name)