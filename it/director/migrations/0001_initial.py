# Generated by Django 5.1.4 on 2025-06-02 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название шаблона')),
                ('description', models.TextField(verbose_name='Описание')),
                ('max_assigned_users', models.PositiveIntegerField(default=1, verbose_name='Максимальное количество исполнителей')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Шаблон задачи',
                'verbose_name_plural': 'Шаблоны задач',
            },
        ),
    ]
