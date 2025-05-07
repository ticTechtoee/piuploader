from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image
import os
from io import BytesIO

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image_file = request.FILES['image']
        file_name = image_file.name
        file_ext = os.path.splitext(file_name)[1].lower()

        image = Image.open(image_file)

        if image.mode in ("RGBA", "P") and file_ext in ['.jpg', '.jpeg']:
            image = image.convert("RGB")

        # Resize large images
        max_size = (1920, 1080)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Create upload path
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file_name)

        # Compress and save
        if file_ext in ['.jpg', '.jpeg']:
            image.save(file_path, format='JPEG', quality=70, optimize=True)
        elif file_ext == '.png':
            image.save(file_path, format='PNG', optimize=True, compress_level=9)
        else:
            # For unsupported formats, save as-is
            image.save(file_path)

        file_url = f"{settings.MEDIA_URL}uploads/{file_name}"
        return JsonResponse({'status': 'success', 'url': file_url})

    return JsonResponse({'status': 'error', 'message': 'No image found'}, status=400)
