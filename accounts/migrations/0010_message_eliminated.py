# Generated by Django 4.2 on 2023-05-10 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_friends_name_save'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='eliminated',
            field=models.CharField(choices=[('el_none', 'None Eliminated'), ('el_sender', 'Sender Eliminated'), ('el_recipient', 'Recipient Eliminated')], default='el_none', max_length=20),
        ),
    ]
