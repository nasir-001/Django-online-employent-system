# Generated by Django 3.0 on 2021-07-05 13:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0003_delete_fileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='qualification',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]