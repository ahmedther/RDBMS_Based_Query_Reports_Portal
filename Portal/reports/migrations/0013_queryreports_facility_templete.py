# Generated by Django 4.1.7 on 2023-03-28 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0012_queryreports_dropdown_option_name1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='queryreports',
            name='facility_templete',
            field=models.BooleanField(blank=True, default=False, verbose_name='Facility Template'),
        ),
    ]