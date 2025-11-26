from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Expense, Category, UserProfile


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['currency']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")