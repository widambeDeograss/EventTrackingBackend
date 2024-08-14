from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([Event, Ticket, Comment, Like, Follow, Notification, EventSetupRequest])
