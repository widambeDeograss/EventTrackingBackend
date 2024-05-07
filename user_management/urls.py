from django.urls import path
from .views import *

app_name = 'user_management'

urlpatterns = [
    path('register', RegisterUser.as_view()),
    path('login', LoginView.as_view()),
    path('user-information', UserInformation.as_view()),
    path('change-password', ChangePasswordView.as_view()),
    path('update-user', UpdateUserView.as_view()),
    path('current_loogged_user', LoggedInUser.as_view()),
    path('change-role', UserChangeRoles.as_view())
]