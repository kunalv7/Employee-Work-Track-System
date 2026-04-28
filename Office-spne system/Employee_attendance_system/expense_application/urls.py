from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('expense_home/', views.expense_home, name='expense_home'),

    # Add Expense Form
    path('add_expense/', views.add_expense, name='add_expense'),

    # Recent Expenses List (card UI page)
    path('recent_expenses/', views.recent_expenses, name='recent_expenses'),

    # Add Voucher (optional page)
    path('add_voucher/', views.add_voucher, name='add_voucher'),

    # 🔥 (Optional but recommended) Expense Detail Page
    path('expense/<int:id>/', views.expense_detail, name='expense_detail'),
]