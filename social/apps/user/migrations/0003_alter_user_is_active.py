# Generated by Django 4.0.2 on 2022-02-18 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_friends_remove_user_waiting_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='active'),
        ),
    ]
