from django.urls import path

from .views import UserView, EntriesView, EntryDetailView


app_name = "mainquickapi"

urlpatterns = [
    path('entries/', EntriesView.as_view()),  # List all user entries endpoint
    path('entries/<int:pk>', EntryDetailView.as_view()),  # Retrieve specified user entry endpoint
    path('users/<int:pk>', UserView.as_view()),  # Retrieve specified user data endpoint
]
