from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # تعریف نقش‌ها به صورت گزینه‌ای (Choices)
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        SELLER = 'SELLER', 'Seller'
        CUSTOMER = 'CUSTOMER', 'Customer'

    # فیلد نقش کاربر که به صورت پیش‌فرض روی مشتری ست شده است
    role = models.CharField(
        max_length=10, 
        choices=Roles.choices, 
        default=Roles.CUSTOMER
    )
    
    # فیلدهای اضافی که بعداً برای فروشنده‌ها یا مشتری‌ها نیاز داری
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name="شماره تماس")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
