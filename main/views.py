from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Brand, City, BrandTicker, BrandsPageSettings
import json
from django.views.decorators.cache import cache_page

# Create your views here.

def home(request):
    current_city_id = request.session.get('current_city_id')
    if current_city_id:
        latest_brands = Brand.objects.filter(location_id=current_city_id).order_by('-id')[:4]
        current_city = City.objects.get(id=current_city_id).name
    else:
        latest_brands = Brand.objects.all().order_by('-id')[:4]
        current_city = None
    
    context = {
        'latest_brands': latest_brands,
        'cities': City.objects.filter(is_active=True).order_by('order', 'name'),
        'current_city': current_city
    }
    return render(request, 'main/home.html', context)

def get_cities(request):
    return City.objects.filter(is_active=True).order_by('order', 'name')

def set_city(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        city_id = data.get('city_id')
        if city_id:
            request.session['current_city_id'] = city_id
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

def brands(request):
    current_city_id = request.session.get('current_city_id')
    if current_city_id:
        brands = Brand.objects.filter(location_id=current_city_id)
        current_city = City.objects.get(id=current_city_id).name
    else:
        brands = Brand.objects.all()
        current_city = None
    
    ticker_texts = BrandTicker.objects.filter(is_active=True)
    page_settings = BrandsPageSettings.objects.first() or BrandsPageSettings.objects.create()
    
    context = {
        'brands': brands,
        'cities': City.objects.filter(is_active=True).order_by('order', 'name'),
        'current_city': current_city,
        'ticker_texts': ticker_texts,
        'page_settings': page_settings,
    }
    return render(request, 'main/brands.html', context)

def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    current_city_id = request.session.get('current_city_id')
    current_city = City.objects.get(id=current_city_id).name if current_city_id else None
    
    context = {
        'brand': brand,
        'cities': City.objects.filter(is_active=True).order_by('order', 'name'),
        'current_city': current_city,
        'top_gallery': brand.top_gallery.all(),
        'bottom_gallery': brand.bottom_gallery.all()
    }
    return render(request, 'main/brand_detail.html', context)
