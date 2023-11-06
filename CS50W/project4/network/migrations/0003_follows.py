# Generated by Django 4.1.5 on 2023-06-08 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_follows', to=settings.AUTH_USER_MODEL)),
                ('user_followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_being_followed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]