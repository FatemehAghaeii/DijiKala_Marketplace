from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}  # پر شدن خودکار اسلاگ بر اساس عنوان


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'stock', 'created_at')
    # فیلتر بر اساس دسته‌بندی و فروشنده برای نمایش دسته‌بندی‌شده محصولات
    list_filter = ('category', 'seller', 'created_at')
    search_fields = ('title', 'description')

from .models import Cart, CartItem

# این بخش باعث می‌شود آیتم‌های سبد خرید، به صورت خطی داخل خود صفحه سبد خرید نمایش داده شوند (خیلی شیک و دیجی‌کالایی!)
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_paid')
    list_filter = ('is_paid', 'created_at')
    inlines = [CartItemInline]  # نمایش آیتم‌ها در داخل سبد خرید    