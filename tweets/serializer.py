from django.conf import settings

from .models import Tweet
from rest_framework import serializers

MAX_TWEET_LENGHT = settings.MAX_TWEET_LENGHT
TWEET_ACTIONS_OPTIONS = settings.TWEET_ACTIONS_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if value not in TWEET_ACTIONS_OPTIONS:
            raise serializers.ValidationErrors("This is not a valid action on tweet!!")
        return value
class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']

        def validate_content(self, value):
            if len(value) > MAX_TWEET_LENGHT:
                raise serializers.ValidationError('The tweet is too long!!')
            return value