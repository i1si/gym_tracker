# Generated by Django 5.0.4 on 2024-04-29 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_customuser_managers_alter_customuser_photo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinishedTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(verbose_name='Старт')),
                ('finished_at', models.DateTimeField(verbose_name='Финиш')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.training')),
            ],
            options={
                'verbose_name': 'Выполненная тренировка',
                'verbose_name_plural': 'Выполненные тренировки',
            },
        ),
    ]
