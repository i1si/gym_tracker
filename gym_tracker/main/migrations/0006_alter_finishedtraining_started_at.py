# Generated by Django 5.0.4 on 2024-05-04 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finishedtraining',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Старт'),
        ),
    ]
