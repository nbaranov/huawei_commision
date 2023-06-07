from django.views.generic import ListView

from .models import Category, Command, Device


class CommandsView(ListView):
    model = Command
    template_name = 'templates/commision/index.html'
    context_object_name = 'commands'
    queryset = Command.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categoryes"] = Category.objects.all().order_by('-id')
        context["devices"] = Device.objects.all().order_by('name')
        return context