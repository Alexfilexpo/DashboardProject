from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import LastProcessedEntry, EntryDetailResults


app_name = 'ceretaidash'

urlpatterns = [
    path('user/', include('django.contrib.auth.urls')),
    path('', LastProcessedEntry.as_view(), name='general'),
    path('detailed-results/<str:date>', EntryDetailResults.as_view(), name='results_detail'),
]