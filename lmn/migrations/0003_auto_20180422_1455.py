# Generated by Django 2.0.3 on 2018-04-22 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lmn', '0002_auto_20180417_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='last_name',
        ),
    ]
