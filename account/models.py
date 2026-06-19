from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'مدیر اصلی'),
        ('SELLER', 'فروشنده'),
        ('CUSTOMER', 'مشتری'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CUSTOMER', verbose_name="نقش کاربری")
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name="شماره تلفن")

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"