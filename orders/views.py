from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart  # <--- کلاس سبد خرید رو صدا زدیم
from django.contrib.auth.decorators import login_required

def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        # اگر مشتری دکمه ثبت رو زد
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 1. ثبت اطلاعات کلی سفارش (اسم و آدرس و...)
            order = form.save()
            
            if request.user.is_authenticated:
                order.user = request.user
            
            order.save()

            # 2. انتقال آیتم‌های سبد خرید به دیتابیس
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    variant=item['variant']
                )
            
            # 3. خالی کردن سبد خرید
            cart.clear()
            
            # 4. نمایش پیام موفقیت
            return render(request, 'orders/created.html', {'order': order})
            
    else:
        # اگر تازه وارد صفحه شده (GET)، فرم خالی نشون بده
        form = OrderCreateForm()
        
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

@login_required
def order_detail(request, order_id):
    # فقط سفارشی رو بگیر که هم IDش درسته، هم مالِ این کاربره (امنیت ۱۰۰٪)
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})