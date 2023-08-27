# Generated by Django 4.2.3 on 2023-07-18 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название категории', max_length=10, verbose_name='Название категории')),
                ('description', models.TextField(help_text='Введите описание категории', max_length=100, verbose_name='Описание категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='Nomination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название номинации', max_length=50, verbose_name='Название номинации')),
            ],
            options={
                'verbose_name': 'Номинация',
                'verbose_name_plural': 'Номинации',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WinnerNomination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField(choices=[(1, 'Первое'), (2, 'Второе'), (3, 'Третье')])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.category')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.member')),
                ('nomination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.nomination')),
            ],
        ),
        migrations.CreateModel(
            name='WinnerCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField(choices=[(1, 'Первое'), (2, 'Второе'), (3, 'Третье')])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.category')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.member')),
            ],
        ),
    ]