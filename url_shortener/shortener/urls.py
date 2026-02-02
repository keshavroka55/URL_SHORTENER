from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_url, name='create'),
    path('edit/<int:id>/', views.edit_url, name='edit'),
    path('delete/<int:id>/', views.delete_url, name='delete'),
    path('qr/<str:short_key>/', views.qr_code, name='qr'),
]
