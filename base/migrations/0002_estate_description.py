# Generated by Django 4.2.7 on 2024-05-21 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estate',
            name='description',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
    ]
