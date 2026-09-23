from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone

from .models import Expense, Budget
from .forms import ExpenseForm, BudgetForm


# ==========================================
# DASHBOARD
# ==========================================

def expense_list(request):

    # ==========================================
    # GET FILTER VALUES
    # ==========================================

    search = request.GET.get(
        'search',
        ''
    ).strip()

    category = request.GET.get(
        'category',
        ''
    ).strip()

    transaction_type = request.GET.get(
        'type',
        ''
    ).strip()

    start_date = request.GET.get(
        'start_date',
        ''
    ).strip()

    end_date = request.GET.get(
        'end_date',
        ''
    ).strip()


    # ==========================================
    # FILTER TRANSACTIONS
    # ==========================================

    filtered_expenses = Expense.objects.all()


    if search:

        filtered_expenses = filtered_expenses.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )


    if category:

        filtered_expenses = filtered_expenses.filter(
            category=category
        )


    if transaction_type:

        filtered_expenses = filtered_expenses.filter(
            type=transaction_type
        )


    if start_date:

        filtered_expenses = filtered_expenses.filter(
            date__gte=start_date
        )


    if end_date:

        filtered_expenses = filtered_expenses.filter(
            date__lte=end_date
        )


    # ==========================================
    # TRANSACTIONS
    # ==========================================

    expenses = filtered_expenses.order_by(
        '-date',
        '-id'
    )


    # ==========================================
    # TOTAL INCOME
    # ==========================================

    total_income = filtered_expenses.filter(

        type='Income'

    ).aggregate(

        total=Sum('amount')

    )['total'] or 0


    # ==========================================
    # TOTAL EXPENSE
    # ==========================================

    total_expense = filtered_expenses.filter(

        type='Expense'

    ).aggregate(

        total=Sum('amount')

    )['total'] or 0


    # ==========================================
    # BALANCE
    # ==========================================

    balance = total_income - total_expense


    # ==========================================
    # CATEGORY ANALYSIS
    # ==========================================

    category_data = filtered_expenses.filter(

        type='Expense'

    ).values(

        'category'

    ).annotate(

        total=Sum('amount')

    ).order_by(

        '-total'

    )


    # ==========================================
    # CATEGORY PERCENTAGES
    # ==========================================

    for item in category_data:

        if total_expense > 0:

            item['percentage'] = round(

                (
                    float(item['total'])
                    /
                    float(total_expense)
                ) * 100

            )

        else:

            item['percentage'] = 0


    # ==========================================
    # TOP CATEGORY
    # ==========================================

    top_category = (

        category_data[0]

        if category_data

        else None

    )


    # ==========================================
    # MONTHLY EXPENSE DATA
    # ==========================================

    monthly_data = (

        filtered_expenses

        .filter(
            type='Expense'
        )

        .annotate(
            month=TruncMonth('date')
        )

        .values(
            'month'
        )

        .annotate(
            total=Sum('amount')
        )

        .order_by(
            'month'
        )

    )


    # ==========================================
    # CURRENT DATE
    # ==========================================

    today = timezone.localdate()


    # ==========================================
    # CURRENT MONTH
    # ==========================================

    current_month_start = today.replace(
        day=1
    )


    # ==========================================
    # CURRENT MONTH BUDGET
    # ==========================================

    current_budget = Budget.objects.filter(

        month=current_month_start

    ).first()


    if current_budget:

        budget_amount = current_budget.amount

    else:

        budget_amount = 0


    # ==========================================
    # CURRENT MONTH EXPENSE
    # ==========================================

    current_month_expense = Expense.objects.filter(

        type='Expense',

        date__year=today.year,

        date__month=today.month

    ).aggregate(

        total=Sum('amount')

    )['total'] or 0


    # ==========================================
    # REMAINING BUDGET
    # ==========================================

    budget_remaining = (
        budget_amount -
        current_month_expense
    )


    # ==========================================
    # BUDGET PERCENTAGE
    # ==========================================

    if budget_amount > 0:

        budget_percentage = round(

            (
                float(current_month_expense)
                /
                float(budget_amount)
            ) * 100

        )

    else:

        budget_percentage = 0


    # ==========================================
    # BUDGET BAR
    # ==========================================

    budget_bar_percentage = min(
        budget_percentage,
        100
    )


    # ==========================================
    # BUDGET STATUS
    # ==========================================

    if budget_amount == 0:

        budget_status = 'No Budget Set'

    elif budget_percentage >= 100:

        budget_status = 'Budget Exceeded'

    elif budget_percentage >= 80:

        budget_status = 'Almost Reached'

    else:

        budget_status = 'Within Budget'


    # ==========================================
    # CONTEXT
    # ==========================================

    context = {

        'expenses': expenses,

        'total_income': total_income,

        'total_expense': total_expense,

        'balance': balance,

        'category_data': category_data,

        'top_category': top_category,

        'monthly_data': monthly_data,

        # Budget
        'current_budget': current_budget,

        'budget_amount': budget_amount,

        'current_month_expense':
            current_month_expense,

        'budget_remaining':
            budget_remaining,

        'budget_percentage':
            budget_percentage,

        'budget_bar_percentage':
            budget_bar_percentage,

        'budget_status':
            budget_status,

        'current_month':
            today.strftime('%B %Y'),

        # Filters
        'search': search,

        'selected_category':
            category,

        'selected_type':
            transaction_type,

        'start_date':
            start_date,

        'end_date':
            end_date,

    }


    return render(

        request,

        'expenses/expense_list.html',

        context

    )


# ==========================================
# SET MONTHLY BUDGET
# ==========================================

def set_budget(request):

    # ==========================================
    # CURRENT MONTH
    # ==========================================

    today = timezone.localdate()

    current_month_start = today.replace(
        day=1
    )


    # ==========================================
    # FIND EXISTING BUDGET
    # ==========================================

    existing_budget = Budget.objects.filter(

        month=current_month_start

    ).first()


    # ==========================================
    # POST
    # ==========================================

    if request.method == 'POST':

        form = BudgetForm(

            request.POST,

            instance=existing_budget

        )


        if form.is_valid():

            budget = form.save()

            return redirect(
                'expense_list'
            )


    # ==========================================
    # GET
    # ==========================================

    else:

        if existing_budget:

            form = BudgetForm(

                instance=existing_budget

            )

        else:

            form = BudgetForm(

                initial={

                    'month':
                        current_month_start

                }

            )


    # ==========================================
    # CONTEXT
    # ==========================================

    context = {

        'form': form,

        'title': 'Set Monthly Budget',

        'current_month':
            today.strftime('%B %Y'),

    }


    return render(

        request,

        'expenses/budget_form.html',

        context

    )


# ==========================================
# ADD TRANSACTION
# ==========================================

def add_expense(request):

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST
        )


        if form.is_valid():

            form.save()

            return redirect(
                'expense_list'
            )


    else:

        form = ExpenseForm()


    context = {

        'form': form,

        'title': 'Add Transaction',

    }


    return render(

        request,

        'expenses/expense_form.html',

        context

    )


# ==========================================
# EDIT TRANSACTION
# ==========================================

def edit_expense(request, id):

    expense = get_object_or_404(

        Expense,

        id=id

    )


    if request.method == 'POST':

        form = ExpenseForm(

            request.POST,

            instance=expense

        )


        if form.is_valid():

            form.save()

            return redirect(
                'expense_list'
            )


    else:

        form = ExpenseForm(

            instance=expense

        )


    context = {

        'form': form,

        'title': 'Edit Transaction',

        'expense': expense,

    }


    return render(

        request,

        'expenses/expense_form.html',

        context

    )


# ==========================================
# DELETE TRANSACTION
# ==========================================

def delete_expense(request, id):

    expense = get_object_or_404(

        Expense,

        id=id

    )


    if request.method == 'POST':

        expense.delete()

        return redirect(
            'expense_list'
        )


    context = {

        'expense': expense,

    }


    return render(

        request,

        'expenses/delete_confirm.html',

        context

    )