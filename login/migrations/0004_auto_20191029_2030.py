# Generated by Django 2.2.6 on 2019-10-29 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20191029_2027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['c_time'], 'verbose_name': '管理员用户', 'verbose_name_plural': '管理员用户'},
        ),
    ]