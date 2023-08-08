# Generated by Django 4.2.3 on 2023-07-19 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_eventstaff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membernomination',
            old_name='nomination',
            new_name='category_nomination',
        ),
        migrations.RemoveField(
            model_name='eventstaff',
            name='event',
        ),
        migrations.AddField(
            model_name='eventstaff',
            name='category_nomination',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='events.categorynomination'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(help_text='Введите название мероприятия', max_length=50, verbose_name='Название мероприятия'),
        ),
        migrations.AlterField(
            model_name='membernomination',
            name='result',
            field=models.JSONField(blank=True, default=[]),
        ),
    ]
