# Generated by Django 3.1.6 on 2021-02-20 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210219_1821'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('first_name', models.CharField(default='', max_length=255)),
                ('last_name', models.CharField(default='', max_length=255)),
                ('username', models.CharField(default='', max_length=255)),
                ('language_code', models.CharField(default='', max_length=64)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
