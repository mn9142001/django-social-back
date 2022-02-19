# Generated by Django 4.0.2 on 2022-02-19 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='obj_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notifications',
            name='obj_type',
            field=models.IntegerField(choices=[(1, 'post'), (2, 'comment'), (3, 'profile')], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notifications',
            name='_context',
            field=models.IntegerField(choices=[(1, 'react'), (2, 'follow'), (3, 'comment'), (4, 'share')]),
        ),
    ]
