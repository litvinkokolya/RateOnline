# Generated by Django 4.2.3 on 2023-08-31 12:00

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=75, scale=None, size=[500, 300], upload_to='images/'),
        ),
    ]