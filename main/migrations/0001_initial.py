# Generated by Django 5.1.6 on 2025-02-06 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='URL')),
                ('subtitle', models.CharField(blank=True, max_length=200, verbose_name='Подзаголовок')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('brand_history', models.TextField(blank=True, verbose_name='История бренда')),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5, verbose_name='Рейтинг')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Телефон')),
                ('whatsapp', models.CharField(blank=True, max_length=20, verbose_name='WhatsApp')),
                ('two_gis', models.URLField(blank=True, verbose_name='2GIS')),
                ('work_hours_weekdays', models.CharField(blank=True, max_length=50, verbose_name='Время работы (Пн-Пт)')),
                ('work_hours_weekends', models.CharField(blank=True, max_length=50, verbose_name='Время работы (Сб-Вс)')),
                ('hero_image', models.ImageField(blank=True, upload_to='brands/hero/', verbose_name='Hero изображение (верхний баннер)')),
                ('main_image', models.ImageField(blank=True, upload_to='brands/main/', verbose_name='Главное изображение (карточка)')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название города')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('order', models.IntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='BottomGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='brands/bottom_gallery/', verbose_name='Изображение')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bottom_gallery', to='main.brand')),
            ],
            options={
                'verbose_name': 'Изображение нижней галереи',
                'verbose_name_plural': 'Нижняя галерея',
            },
        ),
        migrations.AddField(
            model_name='brand',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.city', verbose_name='Город'),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='main.brand')),
            ],
            options={
                'verbose_name': 'Особенность',
                'verbose_name_plural': 'Особенности',
            },
        ),
        migrations.CreateModel(
            name='SpecialOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_offers', to='main.brand')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
            },
        ),
        migrations.CreateModel(
            name='TopGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='brands/top_gallery/', verbose_name='Изображение')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='top_gallery', to='main.brand')),
            ],
            options={
                'verbose_name': 'Изображение верхней галереи',
                'verbose_name_plural': 'Верхняя галерея',
            },
        ),
    ]
