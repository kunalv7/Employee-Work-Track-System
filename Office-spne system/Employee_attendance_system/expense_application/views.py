from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm
from .models import Expense


def expense_home(request):
    return render(request, 'expense_application/expense_home.html')


# ADD EXPENSE
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recent_expenses')
    else:
        form = ExpenseForm()

    return render(request, 'expense_application/add_expense.html', {'form': form})


# RECENT EXPENSES
def recent_expenses(request):
    expenses = Expense.objects.all().order_by('-id')
    return render(request, 'expense_application/recent_expenses.html', {
        'expenses': expenses
    })


# ✅ ADD VOUCHER (FILTER LOGIC)
def add_voucher(request):
    expenses = None

    if request.method == 'POST':
        claim_type = request.POST.get('claim_type')
        travel_type = request.POST.get('travel_type')
        city = request.POST.get('city')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        expenses = Expense.objects.all()

        # Apply filters (ALL must match)
        if claim_type:
            expenses = expenses.filter(claim_type=claim_type)

        if travel_type:
            expenses = expenses.filter(travel_type=travel_type)

        if city:
            expenses = expenses.filter(city=city)

        # Date filter (smart handling)
        if from_date and to_date:
            expenses = expenses.filter(date__range=[from_date, to_date])
        elif from_date:
            expenses = expenses.filter(date__gte=from_date)
        elif to_date:
            expenses = expenses.filter(date__lte=to_date)

    return render(request, 'expense_application/add_voucher.html', {
        'expenses': expenses
    })


# ALL EXPENSE LIST
def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'expense_application/expense_list.html', {'expenses': expenses})


# SINGLE EXPENSE DETAIL
def expense_detail(request, id):
    expense = get_object_or_404(Expense, id=id)
    return render(request, 'expense_application/expense_detail.html', {'expense': expense})