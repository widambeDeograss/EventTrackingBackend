from rest_framework import serializers
from .models import User, Event, Follow, Notification, Comment


class EventGetSerializer(serializers.Serializer):
    class Meta:
        model = Event
        fields = "__all__"
        depth = 2


class FollowGetSerializer(serializers.Serializer):
    class Meta:
        model = Follow
        fields = "__all__"
        depth = 2


class NotificationGetSerializer(serializers.Serializer):
    class Meta:
        model = Notification
        fields = "__all__"
        depth = 2


class CommentGetSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = "__all__"
        depth = 2


class EventPostSerializer(serializers.Serializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'location', 'date_time', 'artist']


class FollowPostSerializer(serializers.Serializer):
    class Meta:
        model = Follow
        fields = ['follower', 'artist']


class NotificationPostSerializer(serializers.Serializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'read']


class CommentPostSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'event', 'text', 'created_at']
