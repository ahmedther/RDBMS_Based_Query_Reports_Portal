# Generated by Django 4.1.7 on 2023-03-30 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0018_alter_queryreports_dropdown_options_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='queryreports',
            name='input_tags',
            field=models.TextField(blank=True, null=True, verbose_name='Input Tags'),
        ),
    ]
