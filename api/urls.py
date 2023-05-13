from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home_api'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:user_id>/', UserList.as_view(), name='user_detail'),
    path('users/<int:user_id>/friends/', FriendList.as_view(), name='user_friend_list'),
    path('users/<int:user_id>/friends/<int:friend>/', FriendList.as_view(), name='user_friend_detail'),
    path('users/<int:user_id>/messages/', MessageList.as_view(), name='user_message_list'),
    path('users/<int:user_id>/messages/<int:recipient_id>/', MessageList.as_view(), name='user_message_to_other'),

    path('messages/', MessageList.as_view(), name='message_list'),
    path('friends/', FriendList.as_view(), name='friend_list'),

]