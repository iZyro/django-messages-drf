from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('<int:id>/', HomeView.as_view(), name='chat'),
    path('add_friend/', AddFriendView.as_view(), name='add_friend'),
    path('edit_friend/<int:id>/', EditFriendView.as_view(), name='edit_friend'),
    path('delete_friend/<int:id>/', DeleteFriendView.as_view(), name='delete_friend'),
    path('delete_chat/<int:id>/', DeleteChatView.as_view(), name='delete_chat')
]