from django.urls import path

from .views import UserView, EntriesView, EntryDetailView, SpecificVideoView


app_name = "api"

urlpatterns = [
    # Entries endpoints
    path('entries/', EntriesView.as_view(), name='EntriesListEndpoint'),  # "Get list of all entries"
    path('entries/<int:pk>/', EntryDetailView.as_view(), name='EntryDetailEndpoint'),  # "Get specific entry by id"
    path('entries/<int:user>/last/', SpecificVideoView.as_view(), name='LastVideoEndpoint'),  # "Get users last video overview"
    path('entries/<int:user>/<str:date>/', SpecificVideoView.as_view(), name='FilteredDateVideoEndpoint'),  # "Get specific user video result using date"
    path('entries/<int:user>/<str:title>/', SpecificVideoView.as_view(), name='FilteredTitleVideoEndpoint'),  # "Get specific user video result using title"
    path('entries/<int:user>/<str:date>/<str:title>/', SpecificVideoView.as_view(), name='DateTitleFilteredVideoEndpoint'),  # "Get specific video result using date and title"

    # Users endpoints
    path('users/<int:pk>/', UserView.as_view(), name='UserDetailEndpoint'),  # "Get specific user data by id",
]

