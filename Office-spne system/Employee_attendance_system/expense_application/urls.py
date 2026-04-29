from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('', views.expense_home, name='expense_home'),

    # ADD EXPENSE
    path('add-expense/', views.add_expense, name='add_expense'),

    # RECENT EXPENSES
    path('recent-expenses/', views.recent_expenses, name='recent_expenses'),

    # ADD VOUCHER (SEARCH + RESULT PAGE)
    path('add-voucher/', views.add_voucher, name='add_voucher'),

    # ALL EXPENSE LIST
    path('expense-list/', views.expense_list, name='expense_list'),

    # SINGLE EXPENSE DETAIL
    path('expense/<int:id>/', views.expense_detail, name='expense_detail'),

]