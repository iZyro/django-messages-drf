# Generated by Django 4.2 on 2023-04-10 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_user_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password',
            new_name='Contraseña',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='Email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='Nombre de usuario',
        ),
    ]
