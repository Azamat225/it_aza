# Generated by Django 5.1.4 on 2025-02-27 13:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('manager2', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(default='', max_length=255)),
                ('phone_number', models.CharField(default='', max_length=20)),
                ('post_user', models.CharField(choices=[('improver', 'Практикант'), ('trainee', 'Стажер'), ('specialist', 'Специалист'), ('expert', 'Эксперт'), ('manager', 'Менеджер'), ('unapproved', 'Неутвержденный')], default='unapproved', max_length=20, null=True)),
                ('avatar', models.ImageField(default='static/img/default_avatar.jpg', upload_to='avatars/')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('pending_type', models.CharField(choices=[('improver', 'Практикант'), ('trainee', 'Стажер'), ('specialist', 'Специалист'), ('expert', 'Эксперт'), ('manager', 'Менеджер'), ('unapproved', 'Неутвержденный')], max_length=20, null=True)),
                ('user_type_confirmed', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('confirmation_code', models.CharField(blank=True, max_length=6, null=True)),
                ('confirmation_sent_at', models.DateTimeField(blank=True, null=True)),
                ('big_stavka', models.FloatField(default=0)),
                ('prize', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Премия')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrizeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма премии')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата назначения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prize_history', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
            ],
        ),
        migrations.CreateModel(
            name='PromotionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_post', models.CharField(max_length=255)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager2.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
