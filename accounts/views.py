from .models import *
from .forms import *
from .serializers import *

from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.views.defaults import page_not_found

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.base import TemplateView

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return redirect('accounts:home')

        messages.error(request, "El usuario o contraseña son incorrectos.")
        return redirect('accounts:login')

class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        context = super().get_context_data(**kwargs)
        context['form'] = RegisterForm

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Te has registrado correctamente.')
            return redirect('accounts:login')
            
        else:
            error_message = list(serializer.errors.values())[0][0]
            if error_message:
                messages.error(request, error_message)
                return redirect('accounts:register')
        
class LogoutView(APIView):
    def get(self, request, format = None):
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
            except:
                pass

            logout(request)
        return redirect('accounts:login')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'

    def get(self, request, *args, **kwargs):

        context = super().get_context_data(**kwargs)
        sender = User.objects.get(id=request.user.id)
        data = {}
        
        chats = get_users_with_messages(sender)
        data['chats'] = []

        friends = Friends.objects.filter(user_id=sender.id)
        data['friends'] = friends

        if kwargs.get('id'):

            recipient = User.objects.get(id=kwargs['id'])
            data['recipient'] = recipient


            msgs = Message.objects.filter(Q(sender=sender, recipient=recipient) | Q(sender=recipient, recipient=sender)).order_by('created_at')
            if msgs.first().sender == sender:
                eliminated = 'el_sender'
            else:
                eliminated = 'el_recipient'

            for msg in msgs:
                if msg.eliminated == eliminated or msg.eliminated == 'el_both':
                    msgs = msgs.exclude(id=msg.id)
            
            data['messages'] = msgs
            for msg in data['messages']:
                message_as_read(request.user, recipient, msg.id)
        
        for chat in chats:
            last_message = Message.objects.filter(Q(sender=sender, recipient=chat) | Q(sender=chat, recipient=sender)).last()
            if friends.filter(friend_id=chat.id).exists():
                recipient_name = friends.get(friend_id=chat.id).name_save
                data['chats'].append({
                    'user': chat,
                    'name_save': recipient_name,
                    'last_message': last_message,
                    'is_friend': True,
                })
            else:
                data['chats'].append({
                    'user': chat,
                    'name_save': chat.id,
                    'last_message': last_message,
                    'is_friend': False,
                })

            context['data'] = data

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        r = User.objects.get(id=kwargs['id'])
        serializer = MessageSerializer(data={'sender': request.user.id, 'recipient': r.id,'message': request.POST['msg'], 'is_read': False})
        if serializer.is_valid():
            serializer.save()


        return redirect(reverse('accounts:chat', kwargs={'id': kwargs['id']}))


class AddFriendView(LoginRequiredMixin, APIView):
    def post(self, request, *args, **kwargs):
        data = {'user': request.user.id, 'name_save': request.POST['name_save'], 'friend': request.POST['friend']}

        serializer = AddFriendSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Se agregó un nuevo amigo.')
        else:
            messages.error(request, 'Este usuario ya lo tiene agregado o no existe.')
        
        return redirect('accounts:home', context={f'data.recipient.id = {data.friend}'})

class EditFriendView(LoginRequiredMixin, APIView):
    def post(self, request, *args, **kwargs):
        name = request.POST['edit_name']
        user = User.objects.get(id=request.user.id)
        friend = Friends.objects.get(user=user, friend=kwargs['id'])
        if not name:
            messages.error(request, 'El nombre no puede estar vacío.')
            return redirect(reverse('accounts:chat', kwargs={'id': kwargs['id']}))
        if name == friend.name_save:
            messages.success(request, 'El nombre es el mismo, no se han cambiado los datos.')
            return redirect(reverse('accounts:chat', kwargs={'id': kwargs['id']}))
        friend.name_save = request.POST['edit_name']
        friend.save()
        messages.success(request, 'Se ha editado correctamente.')
        return redirect(reverse('accounts:chat', kwargs={'id': kwargs['id']}))

class DeleteFriendView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        friend = Friends.objects.filter(user=user, friend=kwargs['id']).first()

        if friend:
            print(friend.name_save)
            messages.success(request, f'Se ha eliminado a _{friend.name_save}_ correctamente')
            friend.delete()
            return redirect(reverse('accounts:chat', kwargs={'id': kwargs['id']}))
        return redirect('accounts:home')
    
class DeleteChatView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        sender = User.objects.get(id=request.user.id)
        recipient = User.objects.filter(id=kwargs['id']).first()

        if recipient:
            msgs = Message.objects.filter(Q(sender=sender, recipient=recipient) | Q(sender=recipient, recipient=sender))
            
            if msgs.first().sender == sender:
                eliminated = 'el_sender'
            else:
                eliminated = 'el_recipient'

            for msg in msgs:
                if msg.eliminated == 'el_none':
                    msg.eliminated = eliminated
                elif msg.eliminated == 'el_sender':
                    msg.eliminated = 'el_both'
                elif msg.eliminated == 'el_recipient':
                    msg.eliminated = 'el_both'
                msg.save()

            messages.success(request, 'Se eliminó el chat correctamente.')
        return redirect('accounts:home')



def get_users_with_messages(user):
    messages = Message.objects.filter(Q(sender=user) | Q(recipient=user))
    users_with_messages = set()
    excluded_users = set()

    first_message = messages.first()
    if first_message and first_message.sender == user:
        eliminated = 'el_sender'
    else:
        eliminated = 'el_recipient'

    for message in messages:
        if message.sender != user:
            users_with_messages.add(message.sender_id)
            if message.eliminated == eliminated or message.eliminated == 'el_both':
                excluded_users.add(message.sender_id)
        if message.recipient != user:
            users_with_messages.add(message.recipient_id)
            if message.eliminated == eliminated or message.eliminated == 'el_both':
                excluded_users.add(message.recipient_id)

    for friend in user.friends.all():
        users_with_messages.add(friend.friend_id)
        if friend.friend_id in excluded_users:
            users_with_messages.remove(friend.friend_id)

    users = []
    for user_id in users_with_messages:
        if user_id not in excluded_users:
            users.append(User.objects.get(id=user_id))

    return users




def message_as_read(sender, recipient, msg_id):
    msg = get_object_or_404(Message, id=msg_id)
    if msg.sender == recipient:
        msg.is_read = True
        msg.save()
    return msg

def custom_page_not_found(request, exception):
    response = page_not_found(request, exception=exception)
    if response.status_code == 404:
        return redirect('accounts:login')
    return response