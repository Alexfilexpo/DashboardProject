from django.urls import path

from .views import LastProcessedEntry


app_name = 'ceretaidash'

urlpatterns = [
    path('', LastProcessedEntry.as_view()),
]