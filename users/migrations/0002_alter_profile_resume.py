# Generated by Django 4.0.6 on 2022-07-16 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='resume',
            field=models.FileField(default='default.png', null=True, upload_to='resumes'),
        ),
    ]
