from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User  # 👈 این خط رو حتما اضافه کن

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='آدرس URL')

    class Meta:

        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="دسته‌بندی")
    name = models.CharField(max_length=200, verbose_name="نام لباس")
    slug = models.SlugField(max_length=200, db_index=True, verbose_name="آدرس URL")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="تصویر لباس")
    description = models.TextField(blank=True, verbose_name="توضیحات (جنس پارچه و...)")
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    available = models.BooleanField(default=True, verbose_name="موجود است؟")
    favorites = models.ManyToManyField(User, related_name='favorites', blank=True, verbose_name='لیست علاقه‌مندی‌ها')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # این یعنی: برو به اپ store، ویوی product_detail رو پیدا کن و slug این محصول رو بهش بده
        return reverse('store:product_detail', args=[self.slug])
    

# 1. مدل رنگ (مثل قرمز، آبی)
class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True) # کد رنگ HTML مثلا #FF0000

    def __str__(self):
        return self.name

# 2. مدل سایز (مثل S, M, XL)
class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

# 3. مدل تنوع محصول (قلب تپنده انبارداری)
class Variants(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1) # موجودی انبار برای این رنگ و سایز خاص
    price_override = models.PositiveIntegerField(blank=True, null=True) # اگر این رنگ گرون‌تر بود

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"

# 4. مدل ویژگی‌های خاص (مثل عرض سینه، جنس پارچه)
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=50, verbose_name="نام ویژگی") # مثلا: عرض سینه
    value = models.CharField(max_length=50, verbose_name="مقدار")    # مثلا: 50 سانتی‌متر

    def __str__(self):
        return f"{self.name}: {self.value}"
    
# این مدل برای جدول سایزهاست (مثلاً سایز M چه ابعادی داره)
class SizeChart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='size_charts')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    
    # اینجا ویژگی‌هایی که گفتی رو میذاریم
    chest_width = models.CharField(max_length=50, blank=True, verbose_name="عرض سینه")
    length = models.CharField(max_length=50, blank=True, verbose_name="قد لباس")
    sleeve_length = models.CharField(max_length=50, blank=True, verbose_name="دور آستین")
    # هر فیلد دیگه‌ای خواستی اینجا اضافه کن

    def __str__(self):
        return f"{self.product.name} - {self.size}"
    
class ProductImage(models.Model):
    # ارتباط با محصول اصلی (اگر محصول پاک شه، عکساش هم پاک میشن)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    # محل ذخیره عکس‌ها
    image = models.ImageField(upload_to='products/gallery/%Y/%m/%d', verbose_name='تصویر')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'

    def __str__(self):
        return f"Image for {self.product.name}"
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    # امتیاز از ۱ تا ۵
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)], verbose_name='امتیاز')
    body = models.TextField(verbose_name='نظر شما')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True) # برای تایید یا رد نظر توسط ادمین

    class Meta:
        ordering = ['-created']
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات کاربران'

    def __str__(self):
        return f"{self.user} on {self.product}"