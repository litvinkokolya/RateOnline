# Generated by Django 4.2.3 on 2023-08-03 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_alter_result_options_nominationattribute_max_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='score_retail',
            field=models.JSONField(default=None, null=True),
        ),
    ]