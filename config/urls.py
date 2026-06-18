from django.contrib import admin
from django.urls import path, include
from store.views import (
    home_view, product_detail_view, cart_view, signup_view,
    customer_panel_view, seller_panel_view, payment_view, 
    add_to_cart, remove_from_cart, checkout, create_store
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('product/<int:pk>/', product_detail_view, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('payment/', payment_view, name='payment'),
    path('customer-panel/', customer_panel_view, name='customer_panel'),
    path('seller-panel/', seller_panel_view, name='seller_panel'),
    
    # اکشن‌ها
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('create-store/', create_store, name='create_store'),
    
    # احراز هویت
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]