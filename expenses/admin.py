from django.contrib import admin
from .models import Expense, Budget


# ==========================================
# EXPENSE ADMIN
# ==========================================

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'amount',
        'category',
        'type',
        'date'
    )

    list_filter = (
        'category',
        'type',
        'date'
    )

    search_fields = (
        'title',
        'description'
    )


# ==========================================
# BUDGET ADMIN
# ==========================================

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):

    list_display = (
        'month',
        'amount',
        'created_at'
    )

    list_filter = (
        'month',
    )