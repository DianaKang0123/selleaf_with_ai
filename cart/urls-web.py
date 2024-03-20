from django.urls import path
from cart.views import CartView, CartListAPI, CartAPI, CartCheckoutAPI

app_name = 'cart'


urlpatterns = [
    # 장바구니 페이지 URL
    path('', CartView.as_view(), name='cart'),
    # 장바구니 목록 API URL
    path('list/<int:cart_id>/', CartListAPI.as_view(), name='cart_list'),
    # 장바구니 항목 API URL
    path('<int:detail_id>/', CartAPI.as_view(), name='cart_detail'),
    # 장바구니 결제 API URL
    path('checkout/<int:cart_id>/', CartCheckoutAPI.as_view(), name='cart_checkout'),
]
