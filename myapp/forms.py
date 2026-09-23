from django import forms
from .models import Task

class NameForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)

    roll_number = forms.IntegerField(
        help_text="Enter 6 digit roll number"
    )

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']