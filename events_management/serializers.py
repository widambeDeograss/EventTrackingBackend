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


class EventSerializer(serializers.ModelSerializer):
    artist_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), source='artists')

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'location', 'date_time', 'artist_ids', 'created_at', 'profile',
                  'tickets_amount', 'likes_count', 'type', 'price']
        read_only_fields = ['id', 'created_at', 'likes_count']

    def create(self, validated_data):
        artists_data = validated_data.pop('artists')
        event = Event.objects.create(**validated_data)
        event.artists.set(artists_data)
        return event


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


class SystemStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_events = serializers.IntegerField()
    total_tickets_sold = serializers.IntegerField()
    total_artists = serializers.IntegerField()
    total_follows = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_notifications = serializers.IntegerField()