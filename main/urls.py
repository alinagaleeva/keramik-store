from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('about', views.AboutView.as_view(), name='about'),
    path('shop', views.ProductsListView.as_view(), name='shop'),
    path('plate_page/<int:product_id>/', views.PlateListView.as_view(), name='plate_page'),
    path('bag', login_required(views.BagView.as_view()), name='bag'),
    path('bag/add/<int:product_id>/', views.bag_add, name='bag_add'),
    path('bag/remove/<int:bag_id>/', views.bag_remove, name='bag_remove'),
    path('bag/minus/<int:bag_id>/', views.bag_minus, name='bag_minus'),
    path('bag/plus/<int:bag_id>/', views.bag_plus, name='bag_plus'),
]
