from django.contrib import admin
from .models import Brand, TopGalleryImage, BottomGalleryImage, Feature, SpecialOffer, City, BrandTicker, BrandsPageSettings

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
