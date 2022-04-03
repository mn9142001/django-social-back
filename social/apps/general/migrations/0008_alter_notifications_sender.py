# Generated by Django 4.0.2 on 2022-02-23 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('general', '0007_remove_notifications_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_created_notifies', to=settings.AUTH_USER_MODEL, to_field='email'),
        ),
    ]
