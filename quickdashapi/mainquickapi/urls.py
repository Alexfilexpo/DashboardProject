from django.urls import path

from .views import EntriesView


app_name = "mainquickapi"

urlpatterns = [
    path('entries/', EntriesView.as_view())
]
