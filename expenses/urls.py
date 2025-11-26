from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.expense_create, name='expense_add'),
    path('expenses/<int:pk>/edit/', views.expense_update, name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path('expenses/export/csv/', views.export_expenses_csv, name='expense_export_csv'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_add'),
]
