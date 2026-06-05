from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('pending/', views.pending_approval, name='pending_approval'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-menu/', views.add_menu_item, name='add_menu_item'),
    path('edit-menu/<int:pk>/', views.edit_menu_item, name='edit_menu_item'),
    path('delete-menu/<int:pk>/', views.delete_menu_item, name='delete_menu_item'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
]
