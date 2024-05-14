from rest_framework import serializers
from .models import User, Event, Follow, Notification, Comment, Ticket


class EventGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        depth = 2


class FollowGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
        depth = 2


class NotificationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        depth = 2


class CommentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        depth = 2


class TicketGetSerializer(serializers. ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        depth = 2


class EventPostSerializer(serializers.Serializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'location', 'date_time', 'artist', 'tickets_amount', 'profile']


class FollowPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'artist']


class NotificationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'read']


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'event', 'text']


class TicketPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'event', 'amount', 'number', 'is_active']