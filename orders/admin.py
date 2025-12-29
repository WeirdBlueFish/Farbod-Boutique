from django.contrib import admin
from .models import Order, OrderItem

# این باعث میشه آیتم‌های سفارش رو داخل خود صفحه سفارش ببینی (خیلی کاربردیه)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product', 'variant']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'city', 'paid', 'created']
    list_filter = ['paid', 'created', 'city']
    inlines = [OrderItemInline] # <--- اتصال بخش بالا