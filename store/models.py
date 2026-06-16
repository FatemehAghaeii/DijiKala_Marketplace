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

class Cart(models.Model):
    # متصل کردن سبد خرید به کاربر (هر کاربر یک سبد خرید فعال دارد)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='carts',
        verbose_name="کاربر"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد سبد")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده؟")

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"

    def __str__(self):
        return f"سبد خرید {self.user.username} - {'پرداخت شده' if self.is_paid else 'در جریان'}"


class CartItem(models.Model):
    # متصل شدن به سبد خرید اصلی
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="سبد خرید مربوطه"
    )
    # متصل شدن به محصولی که خریدار انتخاب کرده
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        verbose_name="محصول"
    )
    # تعداد درخواستی از آن محصول
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"

    def __str__(self):
        return f"{self.quantity} عدد از {self.product.title}"
    
    # یک متد باحال برای محاسبه قیمت کل این آیتم (تعداد × قیمت محصول)
    def get_total_price(self):
        return self.quantity * self.product.price