# Generated by Django 5.1.6 on 2025-02-07 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_sitesettings_remove_photoalbum_yandex_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoalbum',
            name='yandex_preview_url',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='photoalbum',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='album_covers/', verbose_name='Обложка'),
        ),
    ]
