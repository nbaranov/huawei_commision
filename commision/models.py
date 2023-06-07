from django.db import models

# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Command(models.Model):
    command = models.CharField(max_length=1024)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default=1)
    for_device = models.ManyToManyField(Device)

    def __str__(self):
        return f"{self.category.name} - {self.command}"
    