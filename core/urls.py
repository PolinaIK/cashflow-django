from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),

    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Страницы управления справочниками
    path('manage/status/', views.manage_status, name='manage_status'),
    path('manage/transaction-types/', views.manage_transaction_types, name='manage_transaction_types'),
    path('manage/transaction-types/delete/<int:type_id>/', views.delete_transaction_type, name='delete_transaction_type'),
]
