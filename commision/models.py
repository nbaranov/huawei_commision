from django.db import models
from django.db.models import TextField

class NonStrippingTextField(TextField):
    """A TextField that does not strip whitespace at the beginning/end of
    it's value.  Might be important for markup/code."""

    def formfield(self, **kwargs):
        kwargs['strip'] = False
        return super(NonStrippingTextField, self).formfield(**kwargs)

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
    ok_if_include = models.CharField(max_length=1024, blank=True, default='')
    ok_if_exclude = models.CharField(max_length=1024, blank=True, default='')
    false_if_include = models.CharField(max_length=1024, blank=True, default='', )
    out_line_limit = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.category.name} - {self.command}"
    