from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem

# ۱. صفحه اصلی با منطق سرچ و فیلتر کالاها
def home_view(request):
    products = Product.objects.all().order_by('-created_at')
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(title__icontains=search_query)
    return render(request, 'home.html', {'products': products})

# ۲. صفحه جزئیات محصول (که ارور بالا به خاطر نبودن این تابع بود!)
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store_detail.html', {'product': product})

# ۳. افزودن کالا به سبد خرید دیتابیس
@login_required(login_url='/accounts/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart')

# ۴. صفحه سبد خرید واقعی کاربر با محاسبه قیمت کل
@login_required(login_url='/accounts/login/')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total_price})

# ۵. حذف کالا از سبد خرید
@login_required(login_url='/accounts/login/')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

# ۶. صفحه پرداخت آزمایشی با پیام تشکر از خرید موفق
@login_required(login_url='/accounts/login/')
def payment_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    
    if request.method == 'POST':
        # ۱. سبد خرید کاربر را پرداخت شده علامت می‌زنیم
        cart.is_paid = True
        cart.save()
        
        # ۲. اینجا نام کاربر (مثل fati) را می‌گیریم تا پیغام شخصی‌سازی شود
        buyer_name = request.user.username
        thanks_message = f"{buyer_name} عزیز، ممنونم که از این مجموعه خرید کردی! ❤️"
        
        # ۳. فرستادن پیام تشکر به صفحه پرداخت
        return render(request, 'payment.html', {'success': True, 'thanks_message': thanks_message})
        
    total_price = sum(item.product.price * item.quantity for item in cart.items.all())
    return render(request, 'payment.html', {'cart': cart, 'total': total_price, 'success': False})

# ۷. پنل کاربری مشتری
@login_required(login_url='/accounts/login/')
def customer_panel_view(request):
    return render(request, 'customer_panel.html', {'customer': {'user': request.user, 'phone': '۰۹۱۲۳۴۵۶۷۸۹', 'id': request.user.id, 'balance': 0}})

# ۸. بقیه توابع کمکی برای دکمه‌های متفرقه قالب استاد
def store_detail_view(request, pk):
    products = Product.objects.all()
    return render(request, 'store_detail.html', {'products': products})

def seller_panel_view(request):
    return render(request, 'seller_panel.html')

def create_store(request):
    return render(request, 'seller_panel.html')

def checkout(request):
    return redirect('payment')