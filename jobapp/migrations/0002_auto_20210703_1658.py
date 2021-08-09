# Generated by Django 3.0 on 2021-07-03 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='document',
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('document', models.FileField(upload_to='documents/')),
                ('docToJob', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Job', to='jobapp.Job')),
            ],
        ),
    ]
