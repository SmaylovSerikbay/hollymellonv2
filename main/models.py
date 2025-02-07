from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from .utils import compress_image

# Create your models here.

class City(models.Model):
    name = models.CharField('Название города', max_length=100)
    is_active = models.BooleanField('Активен', default=True)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Brand(models.Model):
    # Основная информация
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL', unique=True, blank=True)
    subtitle = models.CharField('Подзаголовок', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    brand_history = models.TextField('История бренда', blank=True)
    rating = models.IntegerField('Рейтинг', default=5, choices=[(i, str(i)) for i in range(1, 6)])
    ticker_text = models.TextField(
        verbose_name='Текст бегущей строки',
        blank=True,
        help_text='Каждое слово или фраза с новой строки'
    )

    # Адрес и контакты
    location = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город')
    address = models.CharField('Адрес', max_length=255, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    whatsapp = models.CharField('WhatsApp', max_length=20, blank=True)
    two_gis = models.URLField('2GIS', blank=True)

    # Время работы
    work_hours_weekdays = models.CharField('Время работы (Пн-Пт)', max_length=50, blank=True)
    work_hours_weekends = models.CharField('Время работы (Сб-Вс)', max_length=50, blank=True)

    # Основные изображения
    hero_image = models.ImageField('Hero изображение (верхний баннер)', upload_to='brands/hero/', blank=True)
    main_image = models.ImageField('Главное изображение (карточка)', upload_to='brands/main/', blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # Сжимаем изображения перед сохранением
        if self.hero_image:
            self.hero_image = compress_image(self.hero_image)
        super().save(*args, **kwargs)

class TopGalleryImage(models.Model):
    """Верхняя галерея (слайдер рядом с описанием)"""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='top_gallery')
    image = models.ImageField('Изображение', upload_to='brands/top_gallery/')

    class Meta:
        verbose_name = 'Изображение верхней галереи'
        verbose_name_plural = 'Верхняя галерея'

    def __str__(self):
        return f'Слайд галереи {self.brand.name}'

class BottomGalleryImage(models.Model):
    """Нижняя галерея (справа от специальных предложений)"""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='bottom_gallery')
    image = models.ImageField('Изображение', upload_to='brands/bottom_gallery/')

    class Meta:
        verbose_name = 'Изображение нижней галереи'
        verbose_name_plural = 'Нижняя галерея'

    def __str__(self):
        return f'Изображение галереи {self.brand.name}'

class Feature(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='features')
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Особенность'
        verbose_name_plural = 'Особенности'

    def __str__(self):
        return self.title

class SpecialOffer(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='special_offers')
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return self.title

class BrandTicker(models.Model):
    text = models.CharField(max_length=500, verbose_name="Текст бегущей строки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    hero_image = models.ImageField('Hero изображение', upload_to='brands/hero/', blank=True)

    class Meta:
        verbose_name = "Бегущая строка брендов"
        verbose_name_plural = "Бегущие строки брендов"
        ordering = ['order']

    def __str__(self):
        return self.text[:50]

class BrandsPageSettings(models.Model):
    show_hero = models.BooleanField('Показывать Hero секцию', default=True)
    show_ticker = models.BooleanField('Показывать бегущую строку', default=True)

    class Meta:
        verbose_name = 'Настройки страницы брендов'
        verbose_name_plural = 'Настройки страницы брендов'

    def save(self, *args, **kwargs):
        if not self.pk and BrandsPageSettings.objects.exists():
            return  # Предотвращаем создание более одной записи
        return super(BrandsPageSettings, self).save(*args, **kwargs)

    def __str__(self):
        return 'Настройки страницы брендов'
