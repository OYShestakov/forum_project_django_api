# Generated by Django 3.2.12 on 2022-03-21 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(verbose_name='Body'),
        ),
    ]