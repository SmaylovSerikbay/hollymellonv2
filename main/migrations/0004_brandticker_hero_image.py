# Generated by Django 5.1.6 on 2025-02-07 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_brandticker'),
    ]

    operations = [
        migrations.AddField(
            model_name='brandticker',
            name='hero_image',
            field=models.ImageField(blank=True, upload_to='brands/hero/', verbose_name='Hero изображение'),
        ),
    ]
