# Generated by Django 4.2.1 on 2023-05-23 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_myuser_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='MyUser',
        ),
        migrations.AlterModelTable(
            name='myuser',
            table='myapp_myuser',
        ),
    ]
