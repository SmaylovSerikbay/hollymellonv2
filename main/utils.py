from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def compress_image(image):
    im = Image.open(image)
    output = BytesIO()
    
    # Конвертируем в JPEG и оптимизируем
    if im.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', im.size, (255, 255, 255))
        background.paste(im, mask=im.split()[-1])
        im = background
    
    # Максимальный размер
    MAX_SIZE = (1200, 1200)
    im.thumbnail(MAX_SIZE, Image.LANCZOS)
    
    # Сохраняем с оптимизацией
    im.save(output, format='JPEG', quality=85, optimize=True)
    output.seek(0)
    
    return InMemoryUploadedFile(output, 'ImageField',
                               f"{image.name.split('.')[0]}.jpg",
                               'image/jpeg',
                               sys.getsizeof(output), None) 