from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    # تغییر مهم: قبلا <int:product_id> بود، الان شد <str:item_id>
    path('remove/<str:item_id>/', views.cart_remove_item, name='cart_remove'),
]