from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserLoginForm # 👈 فرم‌های اختصاصی خودمون

# --------------------------
# 1. ثبت‌نام (Register)
# --------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('store:product_list')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

# --------------------------
# 2. ورود (Login)
# --------------------------
def login_view(request):
    if request.method == 'POST':
        # استفاده از فرم لاگین اختصاصی
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('store:product_list')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# --------------------------
# 3. خروج (Logout) - این تابع گم شده بود
# --------------------------
def logout_view(request):
    auth_logout(request)
    return redirect('store:product_list')

# --------------------------
# 4. پروفایل (Profile)
# --------------------------
@login_required
def profile(request):
    orders = request.user.orders.all().order_by('-created')
    return render(request, 'accounts/profile.html', {'orders': orders})