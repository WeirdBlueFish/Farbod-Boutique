from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm
from django.contrib import messages

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            # پیدا کردن کدی که: 1.متنش یکی باشه 2.تاریخش اوکی باشه 3.فعال باشه
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            # ذخیره آیدی کوپن در سشن کاربر
            request.session['coupon_id'] = coupon.id
            messages.success(request, f'کد تخفیف {coupon.discount} درصدی اعمال شد! 🎉')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, 'این کد تخفیف وجود ندارد یا منقضی شده است. 🚫')
            
    return redirect('cart:cart_detail')