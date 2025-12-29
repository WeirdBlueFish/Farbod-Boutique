from decimal import Decimal
from django.conf import settings
from store.models import Product, Variants # <--- Variants اضافه شد
from coupons.models import Coupon

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False, variant=None):
        """
        اضافه کردن محصول به سبد با در نظر گرفتن سایز و رنگ
        """
        product_id = str(product.id)
        
        # ساختن شناسه یکتا برای سبد خرید
        # اگر واریانت داشت، شناسه میشه: "ID_Product-ID_Variant"
        if variant:
            cart_item_id = f"{product_id}-{variant.id}"
            price = variant.price_override if variant.price_override else product.price
            variant_id = variant.id
        else:
            cart_item_id = product_id
            price = product.price
            variant_id = None

        if cart_item_id not in self.cart:
            self.cart[cart_item_id] = {
                'quantity': 0,
                'price': str(price),
                'product_id': product.id,
                'variant_id': variant_id # <--- ذخیره آیدی واریانت
            }
        
        if override_quantity:
            self.cart[cart_item_id]['quantity'] = quantity
        else:
            self.cart[cart_item_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, cart_item_id):
        # حذف بر اساس شناسه ترکیبی
        if cart_item_id in self.cart:
            del self.cart[cart_item_id]
            self.save()

    def __iter__(self):
        """
        بازگرداندن آیتم‌ها همراه با جزئیات محصول و واریانت
        """
        cart = self.cart.copy()

        for item_id, item in cart.items():
            # گرفتن آبجکت محصول اصلی
            product = Product.objects.get(id=item['product_id'])
            item['product'] = product
            
            # گرفتن آبجکت واریانت (اگر وجود داشت)
            item['variant'] = None
            if item['variant_id']:
                try:
                    item['variant'] = Variants.objects.get(id=item['variant_id'])
                except Variants.DoesNotExist:
                    pass

            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['item_id'] = item_id # این کلید برای دکمه حذف لازمه
            
            yield item

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)
    
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()