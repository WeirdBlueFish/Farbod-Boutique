from django.db import models
from store.models import Product, Variants
from django.contrib.auth.models import User # <--- اینو ایمپورت کن

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    email = models.EmailField(verbose_name='ایمیل')
    address = models.CharField(max_length=250, verbose_name='آدرس پستی')
    postal_code = models.CharField(max_length=20, verbose_name='کد پستی')
    city = models.CharField(max_length=100, verbose_name='شهر')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده؟')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name='نام')

    class Meta:
        ordering = ('-created',) # سفارش‌های جدیدتر اول میان
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        # جمع کل قیمت آیتم‌های این سفارش
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, related_name='order_items', on_delete=models.SET_NULL, blank=True, null=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity