from rest_framework import serializers
from .models import GameTemplate


class GameTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameTemplate
        fields = ['id', 'game_type', 'title', 'description', 'default_config']
        read_only_fields = ['id']
