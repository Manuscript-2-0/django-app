from rest_framework import serializers
from app.models import Event


class EventSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at',)
