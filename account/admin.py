from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # ستون‌هایی که در لیست کاربران پنل ادمین می‌بینی
    list_display = ('username', 'email', 'role', 'phone_number', 'is_staff', 'is_superuser')
    
    # فیلتر سمت راست پنل (برای اینکه با یک کلیک، فروشنده‌ها یا مشتری‌ها جدا شوند)
    list_filter = ('role', 'is_staff', 'is_active')
    
    # قابلیت جستجوی سریع کاربران بر اساس نام کاربری یا شماره تماس
    search_fields = ('username', 'phone_number', 'email')
    
    # اضافه کردن فیلدهای سفارشی به بخش ویرایش کاربران
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات تکمیلی مارکت‌پلیس دیجی‌کالا', {'fields': ('role', 'phone_number', 'address')}),
    )
    
    # فیلدهایی که موقع ساختن کاربر جدید از داخل ادمین باید پر شوند
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات تکمیلی مارکت‌پلیس دیجی‌کالا', {'fields': ('role', 'phone_number', 'address')}),
    )