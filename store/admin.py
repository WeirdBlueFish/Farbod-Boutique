from django.contrib import admin
# SizeChart و ProductImage رو اضافه کن
from .models import Category, Product, Variants, Color, Size, ProductFeature, SizeChart, ProductImage
from .models import Review

# --- اینلاین‌های قبلی ---
class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1

class VariantsInline(admin.TabularInline):
    model = Variants
    extra = 1
    show_change_link = True

class SizeChartInline(admin.TabularInline):
    model = SizeChart
    extra = 1

# --- اینلاین جدید برای گالری تصاویر ---
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # به طور پیشفرض ۳ تا جای خالی نشون میده

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'created']
    list_filter = ['available', 'created']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    # 👇 اینلاین جدید رو اینجا به لیست اضافه کن
    inlines = [ProductFeatureInline, VariantsInline, SizeChartInline, ProductImageInline]

# ثبت مدل‌های فرعی
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Variants)
# admin.site.register(ProductImage) # نیازی نیست جداگانه ثبت بشه چون اینلاین شده

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'active', 'created']
    list_filter = ['active', 'created', 'rating']
    search_fields = ['body']
    actions = ['approve_comments']

    # اکشن برای تایید گروهی نظرات
    def approve_comments(self, request, queryset):
        queryset.update(active=True)