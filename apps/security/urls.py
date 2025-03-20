from django.contrib import admin
from django.urls import path
from apps.security.views import CustomLoginView, register_view, profile_view,save_switch_state
from django.views.generic import View
from django.contrib.auth.views import LogoutView

app_name = 'security'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('save_switch_state',save_switch_state,name = 'save_switch_state'),
]