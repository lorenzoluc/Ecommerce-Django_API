from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #home page
    path('', views.home, name = 'home'),
    path('search/', views.product_search, name='product_search'),
    path('category/<str:class_name>/',views.category_details, name='category_detail'),
    #Login Page
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    #User page
    path('user_page/', views.user_settings, name='user_settings'),
    path('user_page/offer_product', views.offer_product, name='offer_product'),
    path('user_page/my_items/', views.my_sales, name='my_items'),
    path('user_page/my_items/<int:purchase_id>/', views.update_status, name='update_status'),
    path('user_page/follow_shoppping', views.follow_shopping, name='follow_shopping'),
    #Product page
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/buy/', views.buy_product, name='buy_product'),
]
