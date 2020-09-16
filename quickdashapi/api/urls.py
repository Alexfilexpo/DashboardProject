from django.urls import path

from .views import UserView, EntriesView, EntryDetailView, SpecificVideoView


app_name = "api"

urlpatterns = [
    path('entries/', EntriesView.as_view(), name='EntriesListEndpoint'),  # Get list of all user entries endpoint
    path('entries/<int:pk>', EntryDetailView.as_view(), name='EntryDetailEndpoint'),  # Get specific user entry endpoint
    path('entries/<int:user>/<str:date_range>', SpecificVideoView.as_view(), name='DateFilteredVideoEndpoint'),  # Get specific video result
    path('entries/<int:user>/<str:title>', SpecificVideoView.as_view(), name='TitleFilteredVideoEndpoint'),  # Get specific video result using title
    path('entries/<int:user>/<str:date_range>/<str:title>', SpecificVideoView.as_view(), name='DateTitleFilteredVideoEndpoint'),  # Get specific video result using date and title
    path('users/<int:pk>', UserView.as_view(), name='UserDetailEndpoint'),  # Get specific user data endpoint,
]
