# Generated by Django 4.1.5 on 2023-06-08 01:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_follows'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follows',
            old_name='user_followed',
            new_name='user_follower',
        ),
        migrations.AlterField(
            model_name='follows',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_follows', to=settings.AUTH_USER_MODEL),
        ),
    ]
