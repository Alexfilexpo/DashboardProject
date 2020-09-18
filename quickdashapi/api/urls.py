from django.urls import path

from .views import UserView, EntriesView, EntryDetailView, SpecificVideoView


app_name = "api"

urlpatterns = [
    # Entries endpoints
    path('entries/', EntriesView.as_view(), name='EntriesListEndpoint'),  # "Get list of all entries"
    path('entries/<int:pk>', EntryDetailView.as_view(), name='EntryDetailEndpoint'),  # "Get specific entry"
    path('entries/<int:user>/<str:title>', SpecificVideoView.as_view(), name='TitleFilteredVideoEndpoint'),  # "Get specific user video result using title"
    path('entries/<int:user>/<str:date_range>', SpecificVideoView.as_view(), name='DateFilteredVideoEndpoint'),  # "Get specific user video result by date"
    path('entries/<int:user>/<str:date_range>/<str:title>', SpecificVideoView.as_view(), name='DateTitleFilteredVideoEndpoint'),  # "Get specific video result using date and title"

    # Users endpoints
    path('users/<int:pk>', UserView.as_view(), name='UserDetailEndpoint'),  # "Get specific user data endpoint",
]

