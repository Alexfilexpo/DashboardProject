from rest_framework import serializers

from .models import Entries, User, SpeechTimeline, Face


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'entry_date', 'description', 'password', 'total_quota', 'total_hours_analysed',
                  'ceretai_user', 'test_user', 'active', 'current_quota', 'name']

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class SpeechTimeLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeechTimeline
        fields = ['video_id', 'total_length', 'total_speech', 'speech_f', 'speech_m', 'timeline']


class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entries
        fields = ['video_id', 'title', 'external_id', 'user', 'entry_date', 'project']

    def create(self, validated_data):
        return Entries.objects.create(**validated_data)


class FaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face
        fields = ['video_id', 'screen_f', 'screen_m', 'screen_n', 'main_f', 'main_m', 'center_f', 'center_m',
                  'confidence_f', 'confidence_m']