from django.contrib import admin

from .models import Command, Category, Device 

# Register your models here.
admin.site.register(Command)
admin.site.register(Category)
admin.site.register(Device)