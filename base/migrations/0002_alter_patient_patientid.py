# Generated by Django 4.2.8 on 2023-12-10 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='PatientID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
