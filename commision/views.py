from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request, ["templates/commision/index.html"])