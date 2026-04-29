from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime


# HOME
def expense_home(request):
    return render(request, 'expense_application/expense_home.html')


# ✅ ADD EXPENSE
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)

        if form.is_valid():
            expense = form.save(commit=False)

            # ✅ Auto सेट करें
            expense.status = 'Pending'

            # ⚠️ SAFE CALCULATION (None handle)
            amount = expense.amount or 0
            rate = expense.conversion_rate or 1
            expense.final_amount = amount * rate

            expense.save()

            return redirect('add_voucher')

        return render(request, 'expense_application/add_expense.html', {
            'form': form
        })

    else:
        form = ExpenseForm()

    return render(request, 'expense_application/add_expense.html', {'form': form})


# ✅ ADD VOUCHER
def add_voucher(request):
    expenses = Expense.objects.none()
    error = None

    if request.method == 'POST':

        # ✅ STEP 1: Selected expenses
        selected_ids = request.POST.getlist('selected_expenses')

        if selected_ids:
            request.session['selected_expenses'] = selected_ids
            request.session.modified = True  # 🔥 IMPORTANT

            return redirect('recent_expenses')

        # ✅ STEP 2: Filters
        claim_type = request.POST.get('claim_type')
        travel_type = request.POST.get('travel_type')
        city = request.POST.get('city')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if all([claim_type, travel_type, city, from_date, to_date]):
            try:
                from_date = datetime.strptime(from_date, "%Y-%m-%d")
                to_date = datetime.strptime(to_date, "%Y-%m-%d")

                expenses = Expense.objects.filter(
                    claim_type=claim_type,
                    travel_type=travel_type,
                    city=city,
                    date__range=[from_date, to_date]
                ).order_by('-id')

            except ValueError:
                error = "❌ Invalid date format"

        else:
            error = "⚠️ Please fill all fields before searching"

    return render(request, 'expense_application/add_voucher.html', {
        'expenses': expenses,
        'error': error
    })


# ✅ RECENT EXPENSES
from collections import defaultdict
from django.db.models import Sum
from django.db.models.functions import TruncMonth

def recent_expenses(request):
    selected_ids = request.session.get('selected_expenses', [])

    if selected_ids:
        expenses = Expense.objects.filter(id__in=selected_ids).order_by('-date')
    else:
        expenses = Expense.objects.none()

    grouped = defaultdict(list)

    for exp in expenses:
        month = exp.date.replace(day=1)
        grouped[month].append(exp)

    monthly_data = []

    for month, items in grouped.items():
        monthly_data.append({
            'month': month,
            'expenses': items,  # 🔥 individual data
            'total_amount': sum(e.amount for e in items),
            'total_final': sum(e.final_amount for e in items),
        })

    monthly_data = sorted(monthly_data, key=lambda x: x['month'], reverse=True)

    return render(request, 'expense_application/recent_expenses.html', {
        'monthly_data': monthly_data
    })


# ✅ MONTHLY DETAIL
def monthly_detail(request, year, month):
    selected_ids = request.session.get('selected_expenses', [])

    if selected_ids:
        expenses = Expense.objects.filter(
            id__in=selected_ids,
            date__year=year,
            date__month=month
        ).order_by('-date')
    else:
        expenses = Expense.objects.none()

    totals = expenses.aggregate(
        total_amount=Sum('amount'),
        total_final=Sum('final_amount')
    )

    month_name = datetime(year, month, 1).strftime('%B %Y')

    return render(request, 'expense_application/monthly_detail.html', {
        'expenses': expenses,
        'total_amount': totals['total_amount'] or 0,
        'total_final': totals['total_final'] or 0,
        'month_name': month_name
    })
