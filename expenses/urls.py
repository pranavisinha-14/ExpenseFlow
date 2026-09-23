from django.urls import path

from . import views


urlpatterns = [

    # ==========================================
    # DASHBOARD
    # ==========================================

    path(
        '',
        views.expense_list,
        name='expense_list'
    ),


    # ==========================================
    # ADD TRANSACTION
    # ==========================================

    path(
        'add/',
        views.add_expense,
        name='add_expense'
    ),


    # ==========================================
    # EDIT TRANSACTION
    # ==========================================

    path(
        'edit/<int:id>/',
        views.edit_expense,
        name='edit_expense'
    ),


    # ==========================================
    # DELETE TRANSACTION
    # ==========================================

    path(
        'delete/<int:id>/',
        views.delete_expense,
        name='delete_expense'
    ),


    # ==========================================
    # SET BUDGET
    # ==========================================

    path(
        'budget/',
        views.set_budget,
        name='set_budget'
    ),

]