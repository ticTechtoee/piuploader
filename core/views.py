from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        file_name = image.name
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        file_url = f"{settings.MEDIA_URL}uploads/{file_name}"
        return JsonResponse({'status': 'success', 'url': file_url})

    return JsonResponse({'status': 'error', 'message': 'No image found'}, status=400)

