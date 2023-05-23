# Generated by Django 4.2.1 on 2023-05-23 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_employeeuser_customeruser_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('user_type', models.CharField(choices=[('employee', 'Employee'), ('customer', 'Customer')], max_length=10)),
            ],
            options={
                'db_table': 'myapp_myuser',
            },
        ),
        migrations.RemoveField(
            model_name='employeeuser',
            name='user',
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_name', models.CharField(max_length=255)),
                ('active_orders_count', models.IntegerField(default=0)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.myuser')),
            ],
        ),
        migrations.AlterField(
            model_name='newcustomerorder',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.employee'),
        ),
        migrations.AlterField(
            model_name='newcustomerorder',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.myuser'),
        ),
        migrations.DeleteModel(
            name='CustomerUser',
        ),
        migrations.DeleteModel(
            name='EmployeeUser',
        ),
    ]
