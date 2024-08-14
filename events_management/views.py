import uuid

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Event, Follow, Notification, Comment, Like
from .serializers import *


class EventSetupViewSet(ListCreateAPIView):
    queryset = EventSetupRequest.objects.all()
    serializer_class = EventSetupSerializer

    def perform_create(self, serializer):
        print(self.request.data)
        print(self.request.data.get('artist'), "--------------------------------------")
        artist_id = self.request.data.get('artist')
        if artist_id is None:
            raise ValueError("artist ID cannot be null")
        serializer.save(artist_id=artist_id)


# def send_event_notification(artist_ids, message):
#         try:
#             print("---------------------------------------------", artist_ids)
#             for arId in artist_ids:
#                 artist_follows = Follow.objects.filter(artist=arId)
#                 for user in artist_follows:
#                     new_message = f"{user.artist.username} " + message
#                     serializedNot = NotificationPostSerializer(data={
#                         'user': user.follower.id,
#                         'message': new_message
#                     })
#                     if serializedNot.is_valid():
#                         serializedNot.save()
#             return True
#         except Follow.DoesNotExist:
#             return False


class EventView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data

        # Extract and validate artist_ids
        artist_ids = data.get('artist_ids', [])
        if isinstance(artist_ids, str):
            artist_ids = artist_ids.split(',')  # Handle case where artist_ids is a comma-separated string

        valid_artist_ids = []
        invalid_artist_ids = []

        for artist_id in artist_ids:
            artist_id = artist_id.strip().strip('"').strip("'")  # Clean up the artist_id
            try:
                uuid_obj = uuid.UUID(artist_id)
                valid_artist_ids.append(str(uuid_obj))
            except ValueError:
                invalid_artist_ids.append(artist_id)

        if invalid_artist_ids:
            return Response({"save": False, "error": f"Invalid UUID formats: {', '.join(invalid_artist_ids)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        data['artist_ids'] = valid_artist_ids

        # Create Event instance
        event = Event(
            name=data.get('name'),
            description=data.get('description'),
            location=data.get('location'),
            date_time=data.get('date_time'),
            profile=data.get('profile'),  # Ensure 'profile' is either a valid file or None
            tickets_amount=data.get('tickets_amount', 100),
            likes_count=data.get('likes_count', 0),
            type=data.get('type', "BongoFleva"),
            price=data.get('price', 10000)
        )
        event.save()

        # Handle ManyToMany field
        if 'artist_ids' in data:
            artists = User.objects.filter(id__in=data['artist_ids'])
            event.artists.set(artists)

        # Notification logic
        event_name = data['name']
        event_date_time = data['date_time']
        event_location = data['location']
        message = f"Has an Event {event_name} on {event_date_time} at {event_location} don't plan to miss, minimal tickets available"

        artist_follows = User.objects.all()

        try:
            artist = User.objects.get(id=data['artist_ids'][0])
        except User.DoesNotExist:
            return Response({"save": False, "error": "Artist not found."}, status=status.HTTP_404_NOT_FOUND)

        notifications_errors = []
        for follower in artist_follows:
            new_message = f"{artist.username} {message}"
            notification_data = {'user': follower.id, 'message': new_message}
            serializedNot = NotificationPostSerializer(data=notification_data)
            if serializedNot.is_valid():
                serializedNot.save()
            else:
                notifications_errors.append(f"Notification error for user {follower.id}: {serializedNot.errors}")

        if notifications_errors:
            return Response({"save": True, "notifications_errors": notifications_errors})

        return Response({"save": True, "event_id": str(event.id)})

    def put(self, request, pk, format=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()

        # Handle artist_ids if present
        artist_ids = data.get('artist_ids', '')
        if artist_ids:
            artist_ids = artist_ids.split(',')
            valid_artist_ids = []
            invalid_artist_ids = []

            for artist_id in artist_ids:
                artist_id = artist_id.strip().strip('"').strip("'")
                try:
                    uuid_obj = uuid.UUID(artist_id)
                    valid_artist_ids.append(str(uuid_obj))
                except ValueError:
                    invalid_artist_ids.append(artist_id)

            if invalid_artist_ids:
                return Response({"error": f"Invalid UUID formats: {', '.join(invalid_artist_ids)}"},
                                status=status.HTTP_400_BAD_REQUEST)

            data['artist_ids'] = valid_artist_ids

        # Validate and update event
        serializer = EventSerializer(event, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update ManyToMany field
            if 'artist_ids' in data:
                artists = User.objects.filter(id__in=data['artist_ids'])
                event.artists.set(artists)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Event.objects.all()
            serialized = EventGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            eventId = request.GET.get("eventId")
            try:
                queryset = Event.objects.get(id=eventId)
            except Event.DoesNotExist:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
            serialized = EventGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk, format=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        artist_ids = data.get('artist_ids', '')
        if artist_ids:
            data.setlist('artist_ids', artist_ids.split(','))

        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Event.objects.all()
            serialized = EventGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            eventId = request.GET.get("eventId")
            queryset = Event.objects.get(id=eventId)
            serialized = EventGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class FollowView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serialized = FollowPostSerializer(data=data)
        if serialized.is_valid():
            user = User.objects.get(id=data['follower'])
            serializedNot = NotificationPostSerializer(data={
                'user': data['artist'],
                'message': f"{user.username} Just Started following you. Keep up with your events"
            })
            if serializedNot.is_valid():
                serializedNot.save()
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def delete(request):
        data = request.data
        try:
            follow = Follow.objects.get(follower=data['follower'], artist=data['artist'])
            follow.delete()
            return Response({"save": True})
        except Follow.DoesNotExist:
            return Response({"save": False})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Follow.objects.all()
            serialized = FollowGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            userId = request.GET.get("userId")
            following = Follow.objects.filter(follower=userId).count()
            followers = Follow.objects.filter(artist=userId).count()
            data = {
                'followers': followers,
                'following': following
            }
            # serialized = FollowGetSerializer(instance=following, many=False)
            return Response(data)
        else:
            return Response({"message": "Specify the querying type"})


class NotificationView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serialized = NotificationPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Notification.objects.all()
            serialized = NotificationGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            notificationId = request.GET.get("userId")
            queryset = Notification.objects.filter(user=notificationId)
            serialized = NotificationGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "delete":
            notificationId = request.GET.get("notificationId")
            queryset = Notification.objects.get(id=notificationId)
            queryset.delete()
            return Response({"save": True})
        else:
            return Response({"message": "Specify the querying type"})


class CommentView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serialized = CommentPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Comment.objects.all()
            serialized = CommentGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            commentId = request.GET.get("eventId")
            queryset = Comment.objects.filter(event=commentId)
            serialized = CommentGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class TicketView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serialized = TicketPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Ticket.objects.all()
            serialized = TicketGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            userId = request.GET.get("userId")
            queryset = Ticket.objects.filter(user=userId)
            print(queryset)
            serialized = TicketGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class LikeEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        user = request.user

        if not Like.objects.filter(event=event, user=user).exists():
            like = Like.objects.create(event=event, user=user)
            event.update_likes_count()
            return Response({"message": "Event liked successfully"})
        else:
            return Response({"message": "You have already liked this event"}, status=400)


class UnlikeEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        user = request.user

        like = Like.objects.filter(event=event, user=user)
        if like.exists():
            like.delete()
            event.update_likes_count()
            return Response({"message": "Event unliked successfully"})
        else:
            return Response({"message": "You have not liked this event"}, status=400)


class SystemStatsView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        total_users = User.objects.count()
        total_artists = User.objects.filter(role=2).count()
        total_events = Event.objects.count()
        total_tickets_sold = Ticket.objects.filter(is_active=True).count()
        total_likes = Like.objects.count()
        total_follows = Follow.objects.count()
        total_comments = Comment.objects.count()
        total_notifications = Notification.objects.count()

        stats = {
            'total_users': total_users,
            'total_events': total_events,
            'total_tickets_sold': total_tickets_sold,
            'total_artists': total_artists,
            'total_follows': total_follows,
            'total_comments': total_comments,
            'total_notifications': total_notifications,
        }

        serializer = SystemStatsSerializer(stats)
        return Response(serializer.data)
