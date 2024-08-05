from django.urls import path
from .views import *
app_name = 'events_management'

urlpatterns = [
    path('events', EventView.as_view(), name='event-list'),
    path('follows', FollowView.as_view(), name='follow-list'),
    path('notifications', NotificationView.as_view(), name='notification-list'),
    path('comments', CommentView.as_view(), name='comment-list'),
    path('tickets', TicketView.as_view(), name='ticket-list'),
    path('event-setup', EventSetupViewSet.as_view(), name='ticket-list'),
    path('events/<int:event_id>/like/', LikeEvent.as_view(), name='like-event'),
    path('events/<int:event_id>/unlike/', UnlikeEvent.as_view(), name='unlike-event'),
    path('system-stats', SystemStatsView.as_view(), name='system-stats'),
    path('events/<uuid:pk>', EventView.as_view(), name='event-detail'),
]
