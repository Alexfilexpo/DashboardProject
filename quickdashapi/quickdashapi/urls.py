from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('ceretaidash.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('mainquickapi.urls')),
]
