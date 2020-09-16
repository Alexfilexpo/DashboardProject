from datetime import date, timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Entries, User
from .serializers import EntriesSerializer, UserSerializer, SpeechTimeLineSerializer, FaceSerializer, AgeAllSerializer,\
    AgeFemaleSerializer, AgeMaleSerializer


class UserView(APIView):
    """
    Retrieve specified user or create new one
    """

    def get(self, request, pk: int) -> Response:
        user = User.objects.get(user_id=pk)
        serializer = UserSerializer(user, many=False)
        return Response({
            'user': serializer.data
        })

    def put(self, request, pk: int) -> Response:
        user = User.objects.get(user_id=pk)
        serializer = UserSerializer(user, data=request.data.get('user'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntriesView(APIView):
    """
    List all Entries results, or create new one
    """

    def get(self, request) -> Response:
        entries = Entries.objects.all()
        serializer = EntriesSerializer(entries, many=True)
        return Response({
            'entries': serializer.data
        })

    def post(self, request) -> Response:
        entry = request.data.get('entry')
        serializer = EntriesSerializer(data=entry)
        if serializer.is_valid(raise_exception=True):
            entry_saved = serializer.save()
            return Response({"success": "Entry '{}' created successfully ".format(entry_saved.title)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EntryDetailView(APIView):
    """
    Retrieve specified entry
    """

    def get(self, request, pk: int) -> Response:
        entry = Entries.objects.get(video_id=pk)
        serializer = EntriesSerializer(entry, many=False)
        return Response({
            'entry': serializer.data
        })

    def put(self, request, pk: int) -> Response:
        entry = Entries.objects.get(video_id=pk)
        serializer = EntriesSerializer(entry, data=request.data.get('entry'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int) -> Response:
        entry = Entries.objects.get(video_id=pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpecificVideoView(APIView):
    def get(self, request, user, date_range=None, title=None):
        counter = 1
        response = {}
        if not date_range:
            entry_date = date.strftime(date.today()-timedelta(days=1), '%Y-%m-%d')
        else:
            entry_date = date_range.split(' - ') if ' - ' in date_range else date_range
        if date_range and title:
            if isinstance(entry_date, str):
                entries = Entries.objects.filter(user_id=user, entry_date=entry_date, title=title)
            else:
                entries = Entries.objects.filter(user_id=user, entry_date__range=entry_date, title=title)
        elif date_range:
            if isinstance(entry_date, str):
                entries = Entries.objects.filter(user_id=user, entry_date=entry_date)
            else:
                entries = Entries.objects.filter(user_id=user, entry_date__range=entry_date)
        for entry in entries:
            speech_time = entry.speechtimeline_set.get()
            face_data = entry.face_set.get()
            age_data = entry.ageall_set.get()
            female_age_data = entry.agefemale_set.get()
            male_age_data = entry.agemale_set.get()
            context = {
                "request": request,
            }
            entry_serializer = EntriesSerializer(entry, context=context)
            speech_time_serializer = SpeechTimeLineSerializer(speech_time, context=context)
            face_serializer = FaceSerializer(face_data, context=context)
            age_all_serializer = AgeAllSerializer(age_data, context=context)
            age_female_serializer = AgeFemaleSerializer(female_age_data, context=context)
            age_male_serializer = AgeMaleSerializer(male_age_data, context=context)
            response['video_' + str(counter)] = {
                'entry': entry_serializer.data,
                'speech_time': speech_time_serializer.data,
                'face_data': face_serializer.data,
                'age_all_data': age_all_serializer.data,
                'age_female_data': age_female_serializer.data,
                'age_male_data': age_male_serializer.data,
            }
            counter += 1
        return Response(response)
