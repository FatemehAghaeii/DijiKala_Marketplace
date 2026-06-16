from django.db import models
from django.conf import settings

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان دسته‌بندی")
    slug = models.SlugField(unique=True, verbose_name="آدرس اسلاگ (به انگلیسی)")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.title


class Product(models.Model):
    # اتصال محصول به فروشنده‌ای که در اپ account ساختیم
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name="فروشنده"
    )
    # اتصال محصول به دسته‌بندی
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='products',
        verbose_name="دسته‌بندی"
    )
    title = models.CharField(max_length=255, verbose_name="نام محصول")
    description = models.TextField(verbose_name="توضیحات محصول")
    price = models.IntegerField(verbose_name="قیمت (تومان)")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی در انبار")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="تصویر محصول")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.title
