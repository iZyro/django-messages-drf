from django.shortcuts import get_object_or_404
from .models import *
from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'    


    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = make_password(validated_data['password'])
        )
        user.save()

        return user
    
    def validate(self, data):
        username = data['username']
        email = data['email']
        password = data['password']
        password2 = data['password2']

        if len(password) < 8:
            raise serializers.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if password != password2:
            raise serializers.ValidationError('Las contraseñas no coinciden.')
        if username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return data
    

class MessageSerializer(serializers.Serializer):
    sender = serializers.IntegerField()
    recipient  = serializers.IntegerField()
    message = serializers.CharField()

    def create(self, validated_data):
        print(validated_data)
        sender = User.objects.get(id=validated_data['sender'])
        recipient = User.objects.get(id=validated_data['recipient'])

        message = Message.objects.create(
            sender = sender,
            recipient = recipient,
            message = validated_data['message']
        )
        message.save()

        return message
    

class AddFriendSerializer(serializers.ModelSerializer):
    class Meta:
       model = Friends
       fields = '__all__'

    def validate(self, data):
        friend_id = data['friend'].id
        get_object_or_404(User, id=friend_id)
        if self.context['request'].user.friends.filter(friend_id=friend_id).exists():
            raise
        
        return data