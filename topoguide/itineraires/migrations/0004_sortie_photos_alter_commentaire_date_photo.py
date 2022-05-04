# Generated by Django 4.0.4 on 2022-04-25 13:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('itineraires', '0003_alter_sortie_date_sortie_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sortie',
            name='photos',
            field=models.ImageField(default=1, upload_to='photos'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='commentaire',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 25, 14, 38, 3, 934496)),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]