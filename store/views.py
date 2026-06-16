from django.shortcuts import render
from .models import Product

def home_view(request):
    # گرفتن تمام محصولات موجود در دیتابیس پستگرس
    products = Product.objects.all().order_by('-created_at')
    
    # فرستادن کالاها به قالب فرانت‌اَند استاد برای نمایش دادن
    return render(request, 'home.html', {'products': products})