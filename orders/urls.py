from django.urls import path

from . import views

urlpatterns = [
    path('shipping/', views.ShippingView.as_view(), name='shipping'),
    path('payment_confirmation/', views.PaymentConfirmationView.as_view(), name='payment_confirmation'),
    path('orders/', views.OrdersProfileView.as_view(), name='orders'),

]
