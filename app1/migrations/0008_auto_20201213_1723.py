# Generated by Django 3.1.3 on 2020-12-13 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_auto_20201213_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(default='', upload_to='media/app1/images/'),
        ),
    ]