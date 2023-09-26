from django.contrib import admin

from .models import Command, Category, Device, Vendor, AutonomicSystem

# Register your models here.
admin.site.register(Command)
admin.site.register(Category)
admin.site.register(Device)
admin.site.register(Vendor)
admin.site.register(AutonomicSystem)