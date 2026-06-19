from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Category, Store
from account.forms import CustomUserCreationForm

# ۱. صفحه اصلی با نوار جستجو و دسته‌بندی‌ها
def home_view(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-created_at')
    
    # فیلتر دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug and category_slug != 'all':
        products = products.filter(category__slug=category_slug)
        
    # باکس جستجو
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(title__icontains=search_query)
        
    return render(request, 'home.html', {
        'products': products, 
        'categories': categories, 
        'current_category': category_slug
    })

# ۲. صفحه ساخت اکانت جدید (Sign In در منطق شما)
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # تشخیص خودکار ادمین اصلی سیستم
            if user.username.lower() == 'admin':
                user.role = 'ADMIN'
                user.is_staff = True
                user.is_superuser = True
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# ۳. صفحه جزئیات کالا
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store_detail.html', {'product': product})

# ۴. افزودن کالا به سبد خرید
@login_required(login_url='/accounts/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock < 1:
        return redirect('home')
        
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            
    return redirect('cart')

# ۵. صفحه نمایش سبد خرید (cart)
@login_required(login_url='/accounts/login/')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_items = cart.items.all()
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total_price})

# ۶. حذف آیتم از سبد خرید
@login_required(login_url='/accounts/login/')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

# ۷. صفحه پرداخت آنلاین و کسر از موجودی انبار
@login_required(login_url='/accounts/login/')
def payment_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_items = cart.items.all()
    
    if request.method == 'POST':
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
        
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    return render(request, 'payment.html', {'cart': cart, 'total': total_price, 'success': False})

# ۸. مدیریت فروشگاه و افزودن/حذف کالا توسط فروشنده
@login_required(login_url='/accounts/login/')
def seller_panel_view(request):
    if request.user.role != 'SELLER':
        return redirect('home')
    stores = Store.objects.filter(owner=request.user)
    return render(request, 'seller_panel.html', {'stores': stores})

@login_required(login_url='/accounts/login/')
def create_store(request):
    if request.method == 'POST' and request.user.role == 'SELLER':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Store.objects.create(owner=request.user, name=name, description=description)
    return redirect('seller_panel')

@login_required(login_url='/accounts/login/')
def add_product_view(request):
    if request.user.role != 'SELLER':
        return redirect('home')
    if request.method == 'POST':
        store_id = request.POST.get('store')
        category_id = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        
        store = get_object_or_404(Store, id=store_id, owner=request.user)
        category = get_object_or_404(Category, id=category_id)
        
        Product.objects.create(
            store=store, seller=request.user, category=category,
            title=title, description=description, price=price, stock=stock
        )
        return redirect('seller_panel')
    
    categories = Category.objects.all()
    stores = Store.objects.filter(owner=request.user)
    return render(request, 'add_product.html', {'categories': categories, 'stores': stores})

@login_required(login_url='/accounts/login/')
def delete_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_superuser or request.user.role == 'ADMIN' or product.seller == request.user:
        product.delete()
    return redirect('home')

def checkout(request):
    return redirect('payment')