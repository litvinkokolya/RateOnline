# Generated by Django 4.2.3 on 2023-07-19 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(help_text='Введите номер телефона пользователя', max_length=11, verbose_name='Номер телефона'),
        ),
    ]
