from django.contrib import admin
from django.urls import path, include
from store.views import (
    home_view,
    product_detail_view,
    cart_view,
    add_to_cart,
    remove_from_cart,
    payment_view,
    seller_panel_view,
    customer_panel_view,
    create_store,
    checkout,
    signup_view,
    add_product_view,
    delete_product_view,  # ۱. ایمپورت تابع حذف
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('product/<int:pk>/', product_detail_view, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    
    path('payment/', payment_view, name='payment'),
    path('checkout/', checkout, name='checkout'),
    
    path('seller-panel/', seller_panel_view, name='seller_panel'),
    path('customer-panel/', customer_panel_view, name='customer_panel'),
    path('create-store/', create_store, name='create_store'),
    path('seller-panel/add-product/', add_product_view, name='add_product'),
    
    # ۲. ثبت نام مسیر اصلی حذف محصول که تمپلیت به دنبال آن می‌گردد:
    path('product/delete/<int:pk>/', delete_product_view, name='delete_product'),
]