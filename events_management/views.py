from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Event, Follow, Notification, Comment, Like
from .serializers import *


class EventView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serialized = EventSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

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
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

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
            notificationId = request.GET.get("notificationId")
            queryset = Notification.objects.get(id=notificationId)
            serialized = NotificationGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
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