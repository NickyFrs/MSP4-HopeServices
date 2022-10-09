from django.urls import path

from . import views

app_name = 'store'  # connect to the namespace in the main urls.py

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.all_products, name='all_products'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
]
