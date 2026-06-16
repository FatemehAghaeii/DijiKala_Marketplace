from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # مشخص کردن ستون‌هایی که در لیست کاربران نمایش داده می‌شوند
    list_display = ('username', 'email', 'role', 'phone_number', 'is_staff')
    # اضافه کردن فیلتر در سمت راست پنل برای تفکیک راحت فروشنده‌ها و مشتری‌ها
    list_filter = ('role', 'is_staff', 'is_active')
    
    # اضافه کردن فیلدهای سفارشی ما (نقش، تلفن، آدرس) به فرم ادمین
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات تکمیلی مارکت‌پلیس', {'fields': ('role', 'phone_number', 'address')}),
    )