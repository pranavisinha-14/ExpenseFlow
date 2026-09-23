from django.db import models


# ==========================================
# EXPENSE MODEL
# ==========================================

class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Education', 'Education'),
        ('Shopping', 'Shopping'),
        ('Entertainment', 'Entertainment'),
        ('Bills', 'Bills'),
        ('Other', 'Other'),
    ]


    TYPE_CHOICES = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]


    title = models.CharField(
        max_length=200
    )


    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )


    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='Expense'
    )


    description = models.TextField(
        blank=True
    )


    date = models.DateField()


    def __str__(self):

        return self.title


# ==========================================
# MONTHLY BUDGET MODEL
# ==========================================

class Budget(models.Model):

    month = models.DateField(
        unique=True
    )


    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return (
            self.month.strftime('%B %Y')
            + ' - ₹'
            + str(self.amount)
        )