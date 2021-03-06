# Generated by Django 4.0.2 on 2022-02-23 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_comment_drag'),
        ('general', '0008_alter_notifications_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]
