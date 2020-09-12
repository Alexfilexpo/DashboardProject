from rest_framework import serializers

from .models import Entries, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'entry_date', 'description', 'password', 'total_quota', 'total_hours_analysed',
                  'ceretai_user', 'test_user', 'active', 'current_quota', 'name']

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entries
        fields = ['video_id', 'title', 'external_id', 'user', 'entry_date', 'project']

    def create(self, validated_data):
        return Entries.objects.create(**validated_data)
