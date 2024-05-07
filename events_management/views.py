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
        serialized = EventPostSerializer(data=data)
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
            followId = request.GET.get("followId")
            queryset = Follow.objects.get(id=followId)
            serialized = FollowGetSerializer(instance=queryset, many=False)
            return Response(serialized.data)
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
            commentId = request.GET.get("commentId")
            queryset = Comment.objects.get(id=commentId)
            serialized = CommentGetSerializer(instance=queryset, many=False)
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