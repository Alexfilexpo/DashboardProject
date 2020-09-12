from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from mainquickapi.models import User, Entries


class LastProcessedEntry(View):
    template_name = 'ceretaidash/general_view.html'

    def get(self, request):
        print(vars(request))
        return render(request, self.template_name, {'entry_list': Entries.objects.all()})