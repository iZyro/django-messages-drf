from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Message(models.Model):
    STATUS = (
        ('el_none', 'None Eliminated'),
        ('el_sender', 'Sender Eliminated'),
        ('el_recipient', 'Recipient Eliminated'),
        ('el_both', 'Both Eliminated')
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    eliminated = models.CharField(max_length=20, choices=STATUS, default='el_none')

    def __str__(self):
        return f'{self.sender} to {self.recipient}'

class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    name_save = models.CharField(max_length=100, null=False)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def save(self, *args, **kwargs):
        if self.user == self.friend:
            raise ValueError("No puede ser amigo de sí mismo.")
        super(Friends, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.friend}"