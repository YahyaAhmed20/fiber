from django.shortcuts import render

from .models import GalleryImage

# Create your views here.


def about(request):
    facility_images = GalleryImage.objects.filter(section='facility')
    product_images = GalleryImage.objects.filter(section='products')

    return render(request, 'about/about.html', {
        'active_page': 'about',
        'facility_images': facility_images,
        'product_images': product_images,
    })


