# Generated by Django 3.1.5 on 2021-01-24 22:00

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210124_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='header_picture',
            field=models.ImageField(default='none', upload_to=blog.models.upload_to),
            preserve_default=False,
        ),
    ]