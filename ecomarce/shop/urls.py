from django.contrib import admin
from django.urls import path
from. import views

urlpatterns = [
    path('',views.shop,name="shop"),
    path('product/',views.product,name="about"),
    path('contact/',views.contact,name="contact"),
    path('tracker/',views.tracker,name='tracker'),
    path('product/<int:myid>',views.productview,name="productview"),
    path('checkout/',views.checkout,name="checkout"),
    path('about/',views.about,name="checkout"),
    path('search/',views.search,name="search"),
    
]
