# Generated by Django 4.1.3 on 2023-06-07 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('A2Core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_reference',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]
