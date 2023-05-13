from accounts.models import *
from accounts.serializers import *

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.db.models import Q

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class HomeView(TemplateView):
    template_name = 'api/home.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return self.queryset.filter(id=user_id)
        return self.queryset.all()
    

class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessagesSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        recipient = self.kwargs.get('recipient')

        if recipient:
            return self.queryset.filter(Q(sender=user_id, recipient=recipient) | Q(sender=recipient, recipient=user_id))
        elif user_id:
            return self.queryset.filter(sender=user_id)
        
        return self.queryset.all()

class FriendList(generics.ListCreateAPIView):
    queryset = Friends.objects.all()
    serializer_class = AddFriendSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        friend = self.kwargs.get('friend')

        if friend:
            return self.queryset.filter(user_id=user_id, friend_id=friend)
        elif user_id:
            return self.queryset.filter(user_id=user_id)
        
        return self.queryset.all()
