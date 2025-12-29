from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review
from .forms import ReviewForm # 👈 این فرم رو باید ساخته باشی
from django.db.models import Q, Avg
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# ==========================================
# 1. صفحه لیست محصولات (فروشگاه)
# ==========================================
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # 1. فیلتر بر اساس دسته‌بندی
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # 2. جستجو (Search)
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # 3. فیلتر قیمت (Min & Max)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # 4. مرتب‌سازی (Sort)
    sort_by = request.GET.get('sort')
    if sort_by == 'cheapest':
        products = products.order_by('price')
    elif sort_by == 'expensive':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created') # پیش‌فرض: جدیدترین

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/product_list.html', context)


# ==========================================
# 2. صفحه جزئیات محصول (تکی) + نظرات
# ==========================================
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    
    # --- بخش گالری و تصاویر ---
    gallery_images = product.images.all()

    # --- بخش واریانت‌ها (رنگ و سایز) برای JS ---
    variants = product.variants.all()
    variants_data = []
    for v in variants:
        variants_data.append({
            'id': v.id,
            'color_id': v.color.id,
            'size_id': v.size.id,
            'quantity': v.quantity,
            'color_name': v.color.name,
            'size_name': v.size.name
        })

    # --- بخش جدول سایز ---
    size_charts = product.size_charts.all()
    charts_data = {}
    for chart in size_charts:
        charts_data[chart.size.id] = {
            'chest': chart.chest_width,
            'length': chart.length,
            'sleeve': chart.sleeve_length
        }
        
    # لیست‌های یکتا برای منوهای کشویی
    colors = set(v.color for v in variants)
    sizes = set(v.size for v in variants)
    
    # مشخصات فنی
    features = product.features.all()

    # --- بخش محصولات مشابه ---
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    # --- بخش نظرات و امتیازدهی ---
    # 1. دریافت نظرات تایید شده
    reviews = product.reviews.filter(active=True)
    
    # 2. میانگین امتیاز
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if avg_rating is None:
        avg_rating = 0
        
    # 3. پردازش فرم نظر جدید
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'نظر شما ثبت شد و پس از تایید نمایش داده می‌شود.')
                return redirect('store:product_detail', slug=slug)
        else:
            return redirect('accounts:login')
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'gallery_images': gallery_images,
        'colors': colors,
        'sizes': sizes,
        'features': features,
        'variants_json': json.dumps(variants_data, cls=DjangoJSONEncoder),
        'charts_json': json.dumps(charts_data, cls=DjangoJSONEncoder),
        'similar_products': similar_products,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
    }
    return render(request, 'store/product_detail.html', context)

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # چک می‌کنیم کاربر تو لیست لایک‌کننده‌ها هست یا نه
    if product.favorites.filter(id=request.user.id).exists():
        product.favorites.remove(request.user) # حذف از علاقه مندی
        messages.success(request, 'محصول از لیست علاقه‌مندی‌ها حذف شد 💔')
    else:
        product.favorites.add(request.user) # افزودن به علاقه مندی
        messages.success(request, 'محصول به علاقه‌مندی‌ها اضافه شد ❤️')

    # رفرش کردن همون صفحه‌ای که توش هستیم
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))