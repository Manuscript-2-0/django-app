from rest_framework import serializers
from app.models import ManuscriptUser, Event


class ManuscriptUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuscriptUser
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at',)
