from django.shortcuts import render, get_object_or_404
from .models import Product

# نمایش صفحه اصلی با قالب استاد
def home_view(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'products': products})

# نمایش جزئیات محصول (اگر استاد قالب store_detail.html را گذاشته)
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store_detail.html', {'product': product})