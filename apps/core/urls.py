from django.contrib import admin
from django.urls import path
from apps.core.views import home,about,shop,shop_single,contact

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'), 
    path('about/', about, name='about'),
    path('shop/', shop, name='shop'),
    path('shop-single/',shop_single, name= "shop-single"),
    path('contact/', contact, name='contact'),  # Add this line to your URL configuration
]
