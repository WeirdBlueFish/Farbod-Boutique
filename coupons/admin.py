from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    # این فیلدها رو توی لیست نشون بده
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    
    # فیلتر بغل صفحه (فعال/غیرفعال و تاریخ)
    list_filter = ['active', 'valid_from', 'valid_to']
    
    # باکس جستجو برای پیدا کردن کد
    search_fields = ['code']