# Generated by Django 4.1.7 on 2023-03-28 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0011_queryreports_sub_sql_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='queryreports',
            name='dropdown_option_name1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='queryreports',
            name='dropdown_option_name2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='queryreports',
            name='dropdown_option_value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
