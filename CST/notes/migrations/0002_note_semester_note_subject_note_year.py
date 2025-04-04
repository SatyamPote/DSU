# Generated by Django 5.0.6 on 2025-02-23 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='semester',
            field=models.CharField(choices=[('1', 'Semester 1'), ('2', 'Semester 2')], default='1', max_length=1),
        ),
        migrations.AddField(
            model_name='note',
            name='subject',
            field=models.CharField(choices=[('math', 'Mathematics'), ('cs', 'Computer Science'), ('eng', 'English')], default='math', max_length=50),
        ),
        migrations.AddField(
            model_name='note',
            name='year',
            field=models.CharField(choices=[('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year')], default='1', max_length=1),
        ),
    ]
