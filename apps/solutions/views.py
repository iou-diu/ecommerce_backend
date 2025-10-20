import os
import uuid

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Solution, Category


def solution_list(request):
    solutions = Solution.objects.all()
    return render(request, 'solution/list.html', {'solutions': solutions})


def solution_add(request):
    return solution_save(request)


def solution_edit(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    return solution_save(request, solution)


import os
import uuid
from django.conf import settings
from django.shortcuts import render, redirect

def solution_save(request, instance=None):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('categories')
        overview = request.POST.get('overview')
        short_description = request.POST.get('short_description')
        key_features = request.POST.getlist('key_features[]')

        tech_keys = request.POST.getlist('technical_keys[]')
        tech_values = request.POST.getlist('technical_values[]')

        faq_keys = request.POST.getlist('faq_keys[]')
        faq_values = request.POST.getlist('faq_values[]')

        description = request.POST.get('description')
        video_url = request.POST.get('video_url')

        technical_features = dict(zip(tech_keys, tech_values))

        faq_list = dict(zip(faq_keys, faq_values))

        if not instance:
            instance = Solution()

        instance.title = title
        instance.categories_id = category_id
        instance.overview = overview
        instance.short_description = short_description
        instance.key_features = key_features
        instance.technical_features = technical_features
        instance.faqs = faq_list
        instance.description = description
        instance.video_url = video_url

        if 'thumbnail' in request.FILES:
            instance.thumbnail = request.FILES['thumbnail']

        instance.save()

        # 🧹 Clean and normalize existing images (strip prefix if present)
        existing_images = set()
        for img_path in request.POST.getlist('existing_images'):
            img_path = img_path.strip()
            if img_path.startswith('/media/'):
                img_path = img_path[len('/media/'):]
            existing_images.add(img_path)

        # 📥 Handle new images
        new_images = set()
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'solutions/images')
        os.makedirs(upload_dir, exist_ok=True)

        for img in request.FILES.getlist('images'):
            ext = os.path.splitext(img.name)[1]
            unique_name = f"{uuid.uuid4().hex}{ext}"
            path = f'solutions/images/{unique_name}'
            full_path = os.path.join(settings.MEDIA_ROOT, path)

            with open(full_path, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)

            new_images.add(path)

        # 🧠 Merge and prefix with /media/ for URLs
        combined_images = existing_images.union(new_images)
        instance.images = [f'/media/{img}' for img in combined_images]
        instance.save()

        return redirect('solution_list')

    context = {
        'object': instance,
        'page_title': 'Solution',
        'list_link': '/solutions/',
        'categories': Category.objects.filter(parent__isnull=False, is_active=True, for_solution=True),
    }
    return render(request, 'solution/add.html', context)

