from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Entries


class EntriesView(APIView):
    def get(self, request):
        entries = Entries.objects.all()
        return Response({'entries': entries})
