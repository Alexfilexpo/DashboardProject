from django.urls import path, include

from .views import LastProcessedEntry, EntryDetailResults


app_name = 'ceretaidash'

urlpatterns = [
    path('', LastProcessedEntry.as_view(), name='general'),
    path('user/', include('django.contrib.auth.urls')),
    path('detailed-results/<str:date>', EntryDetailResults.as_view(), name='results_detail'),
]
