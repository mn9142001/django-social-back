# Generated by Django 4.0.2 on 2022-02-17 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_react_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='drag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_replies', to='blog.comment'),
        ),
    ]
