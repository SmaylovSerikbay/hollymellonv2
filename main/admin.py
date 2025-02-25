from django.contrib import admin
from django import forms
from .models import Brand, TopGalleryImage, BottomGalleryImage, Feature, SpecialOffer, City, BrandTicker, BrandsPageSettings, PhotoAlbum, SiteSettings, Announcement, AnnouncementItem
from .utils import get_yandex_folders

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name',)
    ordering = ['order', 'name']

class TopGalleryInline(admin.TabularInline):
    model = TopGalleryImage
    extra = 1
    verbose_name = 'Изображение верхней галереи'
    verbose_name_plural = 'Верхняя галерея (слайдер)'

class BottomGalleryInline(admin.TabularInline):
    model = BottomGalleryImage
    extra = 1
    verbose_name = 'Изображение нижней галереи'
    verbose_name_plural = 'Нижняя галерея'

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1

class SpecialOfferInline(admin.TabularInline):
    model = SpecialOffer
    extra = 1

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'show_rating')
    list_filter = ('location', 'rating')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name', 'slug', 'subtitle', 'description', 
                'brand_history', 'rating'
            )
        }),
        ('Основные изображения', {
            'fields': (
                'hero_image', 'main_image'
            ),
            'description': 'Hero - для верхнего баннера, Main - для карточки бренда'
        }),
        ('Адрес и контакты', {
            'fields': (
                'location', 'address', 'phone', 
                'whatsapp', 'two_gis'
            )
        }),
        ('Время работы', {
            'fields': ('work_hours_weekdays', 'work_hours_weekends')
        })
    )

    inlines = [TopGalleryInline, BottomGalleryInline, FeatureInline, SpecialOfferInline]

    def show_rating(self, obj):
        return '⭐' * obj.rating
    show_rating.short_description = 'Рейтинг'

@admin.register(BrandTicker)
class BrandTickerAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('text',)
    ordering = ('order',)

@admin.register(BrandsPageSettings)
class BrandsPageSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Запрещаем создание новых настроек, если они уже существуют
        return not BrandsPageSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление настроек
        return False

class PhotoAlbumForm(forms.ModelForm):
    yandex_folder = forms.ChoiceField(
        label='Папка на Яндекс.Диске',
        choices=[],
        help_text='Выберите папку из Яндекс.Диска'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Получаем токен из настроек
        settings = SiteSettings.objects.first()
        if settings and settings.yandex_token:
            folders = get_yandex_folders(settings.yandex_token)
            self.fields['yandex_folder'].choices = [
                (folder['path'].strip('/'), folder['name']) for folder in folders
            ]
        else:
            self.fields['yandex_folder'].choices = [('', 'Сначала добавьте токен в настройках сайта')]

    class Meta:
        model = PhotoAlbum
        fields = '__all__'

@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    form = PhotoAlbumForm
    list_display = ('title', 'city', 'date', 'created_at')
    list_filter = ('city', 'date')
    search_fields = ('title', 'city__name')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        settings = SiteSettings.objects.first()
        if not settings or not settings.yandex_token:
            self.message_user(request, 'Добавьте токен Яндекс.Диска в настройках сайта', level='WARNING')
        return form

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Настройки Яндекс.Диска', {
            'fields': ('yandex_token',),
        }),
        ('О нас', {
            'fields': ('about_text', 'about_image', 'email', 'instagram_link', 'tiktok_link'),
            'description': 'Настройки для секции "О нас" на главной странице'
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

class AnnouncementItemInline(admin.TabularInline):
    model = AnnouncementItem
    extra = 1
    fields = ('title', 'description', 'icon', 'order')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'type')
    search_fields = ('header', 'items__title', 'items__description')
    list_editable = ('is_active', 'order')
    ordering = ('order', '-created_at')
    inlines = [AnnouncementItemInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('type', 'is_active', 'order'),
        }),
        ('Заголовок события', {
            'fields': ('header',),
            'description': 'Заголовок отображается над списком анонсов на главной странице. '
                         'Например: "Готовимся к захватывающему событию: уже [дата] мы ждем вас на [название мероприятия]"'
        }),
    )

    class Media:
        css = {
            'all': ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css']
        }

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'icon':
            field.help_text = field.help_text + ' <br>Доступные иконки можно посмотреть на <a href="https://fontawesome.com/icons" target="_blank">Font Awesome</a>'
        return field
