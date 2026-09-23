from django import forms
from datetime import date

from .models import Expense, Budget


# ==========================================
# EXPENSE FORM
# ==========================================

class ExpenseForm(forms.ModelForm):

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )


    class Meta:

        model = Expense

        fields = [
            'title',
            'amount',
            'category',
            'type',
            'description',
            'date',
        ]


        widgets = {

            'title': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Grocery Shopping'
                }
            ),


            'amount': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter amount',
                    'step': '0.01'
                }
            ),


            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Add a note...',
                    'rows': 4
                }
            ),

        }


# ==========================================
# BUDGET FORM
# ==========================================

class BudgetForm(forms.ModelForm):

    month = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'month'
            }
        )
    )


    class Meta:

        model = Budget

        fields = [
            'month',
            'amount',
        ]


        widgets = {

            'amount': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter monthly budget',
                    'step': '0.01',
                    'min': '0'
                }
            ),

        }


    # ==========================================
    # CONVERT MONTH TO DATE
    # ==========================================

    def clean_month(self):

        month_value = self.cleaned_data['month']


        try:

            year, month = month_value.split('-')


            return date(
                int(year),
                int(month),
                1
            )


        except (ValueError, TypeError):

            raise forms.ValidationError(
                'Please select a valid month.'
            )