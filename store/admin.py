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