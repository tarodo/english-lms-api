# Generated by Django 3.1.6 on 2021-02-24 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='is_student',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='definition',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='example',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='translate',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='WordSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
                ('words', models.ManyToManyField(to='core.Word')),
            ],
        ),
    ]
