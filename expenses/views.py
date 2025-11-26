from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm

from django.db.models.functions import TruncMonth
import json

@login_required
def dashboard(request):
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    # Basic totals
    total_all = Expense.objects.filter(user=request.user).aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    total_this_month = Expense.objects.filter(
        user=request.user,
        date__gte=start_of_month,
        date__lte=today
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Top categories
    by_category_qs = (
        Expense.objects.filter(user=request.user)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # Data for category pie chart
    category_labels = []
    category_totals = []
    for row in by_category_qs:
        category_labels.append(row['category__name'] or "(No category)")
        category_totals.append(float(row['total']))

    # Data for monthly bar chart (last 6 months)
    monthly_qs = (
        Expense.objects.filter(user=request.user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    monthly_labels = []
    monthly_totals = []
    for row in monthly_qs:
        if row['month']:
            monthly_labels.append(row['month'].strftime('%Y-%m'))
            monthly_totals.append(float(row['total']))

    context = {
        'total_all': total_all,
        'total_this_month': total_this_month,
        'by_category': by_category_qs[:5],

        # JSON for Chart.js
        'category_labels_json': json.dumps(category_labels),
        'category_totals_json': json.dumps(category_totals),
        'monthly_labels_json': json.dumps(monthly_labels),
        'monthly_totals_json': json.dumps(monthly_totals),
    }
    return render(request, 'expenses/dashboard.html', context)



from django.core.paginator import Paginator

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)

    category_id = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if category_id:
        expenses = expenses.filter(category_id=category_id)
    if date_from:
        expenses = expenses.filter(date__gte=date_from)
    if date_to:
        expenses = expenses.filter(date__lte=date_to)

    paginator = Paginator(expenses, 10)
    page = request.GET.get('page')
    expenses_page = paginator.get_page(page)

    categories = Category.objects.filter(user=request.user)

    context = {
        'expenses': expenses_page,
        'categories': categories,
        'selected_category': category_id,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'expenses/expense_list.html', context)


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses:expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expenses/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('expenses:category_list')
    else:
        form = CategoryForm()
    return render(request, 'expenses/category_form.html', {'form': form})
