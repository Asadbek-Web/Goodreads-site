# Generated by Django 4.0.5 on 2022-07-21 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='author_picture',
            field=models.ImageField(default='default_cover.jpg', upload_to=''),
        ),
    ]