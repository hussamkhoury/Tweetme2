from django.conf import settings

from .models import Tweet
from rest_framework import serializers

MAX_TWEET_LENGHT = settings.MAX_TWEET_LENGHT
TWEET_ACTIONS_OPTIONS = settings.TWEET_ACTIONS_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if value not in TWEET_ACTIONS_OPTIONS:
            raise serializers.ValidationError("This is not a valid action on tweet!!")
        return value

class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGHT:
            raise serializers.ValidationError('The tweet is too long!!')
        return value

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    original_tweet = TweetCreateSerializer(source='parent',read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'original_tweet']

    def get_likes(self, obj):
        return obj.likes.count()