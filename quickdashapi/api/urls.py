from django.urls import path

from .views import UserView, EntriesView, EntryDetailView, LastEntryDetailView


app_name = "api"

urlpatterns = [
    path('entries/', EntriesView.as_view(), name='EntriesListEndpoint'),  # List all user entries endpoint
    path('entries/<int:pk>', EntryDetailView.as_view(), name='EntryDetailEndpoint'),  # Retrieve specified user entry endpoint
    path('entries/<int:user>/lastentry', LastEntryDetailView.as_view(), name='LastEntryDetailEndpoint'),
    path('users/<int:pk>', UserView.as_view(), name='UserDetailEndpoint'),  # Retrieve specified user data endpoint,
]