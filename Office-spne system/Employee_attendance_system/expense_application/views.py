from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm
from .models import Expense


# HOME
def expense_home(request):
    return render(request, 'expense_application/expense_home.html')


# ✅ ADD EXPENSE (FULL FIXED)
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)

        if form.is_valid():
            expense = form.save(commit=False)

            # 🔥 FIX 1: status auto set
            expense.status = 'Pending'

            # 🔥 FIX 2: final amount auto calculate
            expense.final_amount = expense.amount * expense.conversion_rate

            expense.save()

            print("✅ DATA SAVED SUCCESSFULLY")

            # ✅ Redirect only if saved
            return redirect('add_voucher')

        else:
            print("❌ FORM ERROR:", form.errors)

            # ❌ Stay on same page with errors
            return render(request, 'expense_application/add_expense.html', {
                'form': form
            })

    else:
        form = ExpenseForm()

    return render(request, 'expense_application/add_expense.html', {'form': form})


def add_voucher(request):

    expenses = Expense.objects.none()
    error = None

    if request.method == 'POST':

        # ✅ STEP 1: Check if selected submit
        selected_ids = request.POST.getlist('selected_expenses')

        if selected_ids:
            # 🔥 SAVE IN SESSION
            request.session['selected_expenses'] = selected_ids

            # 👉 redirect to recent page
            return redirect('recent_expenses')

        # ✅ STEP 2: FILTER LOGIC (same as your code)
        claim_type = request.POST.get('claim_type')
        travel_type = request.POST.get('travel_type')
        city = request.POST.get('city')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if claim_type and travel_type and city and from_date and to_date:

            expenses = Expense.objects.filter(
                claim_type=claim_type,
                travel_type=travel_type,
                city=city,
                date__range=[from_date, to_date]
            ).order_by('-id')

        else:
            error = "⚠️ Please fill all fields before searching"

    return render(request, 'expense_application/add_voucher.html', {
        'expenses': expenses,
        'error': error
    })


# ALL EXPENSE LIST
def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'expense_application/expense_list.html', {
        'expenses': expenses
    })


# SINGLE EXPENSE DETAIL
def expense_detail(request, id):
    expense = get_object_or_404(Expense, id=id)
    return render(request, 'expense_application/expense_detail.html', {
        'expense': expense
    })


# RECENT EXPENSES
def recent_expenses(request):

    selected_ids = request.session.get('selected_expenses')

    if selected_ids:
        expenses = Expense.objects.filter(id__in=selected_ids).order_by('-id')
    else:
        expenses = Expense.objects.all().order_by('-id')

    return render(request, 'expense_application/recent_expenses.html', {
        'expenses': expenses
    })