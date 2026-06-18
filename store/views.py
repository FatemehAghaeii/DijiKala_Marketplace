from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Category, Store
from account.forms import CustomUserCreationForm

# ۱. صفحه اصلی همراه با دسته‌بندی‌ها و نوار جستجو
def home_view(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-created_at')
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug and category_slug != 'all':
        products = products.filter(category__slug=category_slug)
        
    # نوار جستجو
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(title__icontains=search_query)
        
    return render(request, 'home.html', {
        'products': products, 
        'categories': categories, 
        'current_category': category_slug
    })

# ۲. صفحه ثبت‌نام سفارشی (Sign Up)
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_allowed_filters_and_valid(): # چک کردن صحت اطلاعات
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# ۳. صفحه جزئیات محصول (توضیحات، عکس، قیمت و مشخصات)
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store_detail.html', {'product': product})

# ۴. افزودن چندتایی به سبد خرید با چک کردن موجودی انبار
@login_required(login_url='/accounts/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.stock < 1:
        return redirect('home') # اگر موجودی صفر بود اجازه نده
        
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            
    return redirect('cart')

# ۵. صفحه سبد خرید (Cart)
@login_required(login_url='/accounts/login/')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total_price})

# ۶. حذف یا کم کردن از سبد خرید
@login_required(login_url='/accounts/login/')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

# ۷. صفحه پرداخت آنلاین و کسر اتوماتیک از موجودی انبار (مدیریت موجودی)
@login_required(login_url='/accounts/login/')
def payment_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_items = cart.items.all()
    
    if request.method == 'POST':
        # کسر از موجودی انبار برای هر محصول خریده شده
        for item in cart_items:
            product = item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()
            else:
                return render(request, 'payment.html', {'error': f"موجودی کالا {product.title} به اتمام رسیده است."})
        
        cart.is_paid = True
        cart.save()
        
        thanks_message = f"{request.user.username} عزیز، ممنونم که از این مجموعه خرید کردی! ❤️"
        return render(request, 'payment.html', {'success': True, 'thanks_message': thanks_message})
        
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'payment.html', {'cart': cart, 'total': total_price, 'success': False})

# ۸. پنل کاربری و ساخت فروشگاه برای فروشندگان
@login_required(login_url='/accounts/login/')
def customer_panel_view(request):
    return render(request, 'customer_panel.html')

@login_required(login_url='/accounts/login/')
def seller_panel_view(request):
    stores = Store.objects.filter(owner=request.user)
    return render(request, 'seller_panel.html', {'stores': stores})

@login_required(login_url='/accounts/login/')
def create_store(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Store.objects.create(owner=request.user, name=name, description=description)
        return redirect('seller_panel')
    return render(request, 'seller_panel.html')

def checkout(request):
    return redirect('payment')