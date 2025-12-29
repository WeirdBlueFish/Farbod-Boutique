from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product, Variants # <--- Variants رو ایمپورت کن
from .cart import Cart
from coupons.forms import CouponApplyForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # گرفتن اطلاعات از فرم (HTML)
    variant_id = request.POST.get('variant') # name="variant" تو فرم HTML
    selected_variant = None
    
    if variant_id:
        selected_variant = get_object_or_404(Variants, id=variant_id)
    
    # اضافه کردن به سبد همراه با واریانت
    cart.add(product=product, quantity=1, variant=selected_variant)
    
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    # نکته: اینجا product_id در واقع همون کلید ترکیبی هست که تو html پاس میدیم
    cart = Cart(request)
    cart.remove(product_item_id=product_id) 
    # صبر کن! اینجا باید یه تغییر کوچیک تو url بدیم که پایین میگم
    return redirect('cart:cart_detail')

# این تابع remove رو باید اصلاح کنیم چون الان ورودیش دیگه فقط عدد نیست (رشته است)
def cart_remove_item(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm() # فرم رو بساز
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})
