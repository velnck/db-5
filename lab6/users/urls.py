from django.urls import path
from .views import (LoginUserView, RegisterUserView,
                    UserProfileView, logout_user, UpdateUserProfileView,
                    UsersView, LogsView, update_user_role)

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/<int:user_id>', UserProfileView.as_view(), name='user-profile'),
    path('update-profile/<int:user_id>', UpdateUserProfileView.as_view(), name='update-profile'),
    path('users/', UsersView.as_view(), name='users'),
    path('logs/', LogsView.as_view(), name='logs'),
    path('update-role/<int:user_id>', update_user_role, name='update-role'),
]