import base64
import io
import urllib

import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from api.models import User, Entries


class LastProcessedEntry(View):
    template_name = 'general_view.html'

    def get(self, request):
        # Creating charts
        labels = 'Women', 'Man', 'Undetermined'
        sizes = [46.5, 52.5, 1]
        fig1, ax1 = plt.subplots()  # Creating simple figure
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)  # Define figure as pie chart
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        chart = plt.gcf()  # Get current figure (chart)
        buffer = io.BytesIO()  # Creating buffer
        chart.savefig(buffer, format='png')  # Saving current chart
        buffer.seek(0)  # Define buffer to be read from start
        chart_sring = base64.b64encode(buffer.read())  # Encoding image to bytes object
        chart_uri = urllib.parse.quote(chart_sring)  # Quoting special characters and encoding non-ASCII text

        return render(request, self.template_name, {'entry_list': Entries.objects.all(), 'chart_uri': chart_uri})

