from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Status, TransactionType, Category, SubCategory
from .forms import TransactionForm, FilterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    form = FilterForm(request.GET or None)
    if form.is_valid():
        if form.cleaned_data['date_from']:
            transactions = transactions.filter(date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data['date_to']:
            transactions = transactions.filter(date__lte=form.cleaned_data['date_to'])
        if form.cleaned_data['status']:
            transactions = transactions.filter(status=form.cleaned_data['status'])
        if form.cleaned_data['transaction_type']:
            transactions = transactions.filter(transaction_type=form.cleaned_data['transaction_type'])
        if form.cleaned_data['category']:
            transactions = transactions.filter(category=form.cleaned_data['category'])
        if form.cleaned_data['subcategory']:
            transactions = transactions.filter(subcategory=form.cleaned_data['subcategory'])
    return render(request, 'core/transaction_list.html', {'transactions': transactions, 'form': form})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'core/add_transaction.html', {'form': form})

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'core/edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'core/delete_transaction.html', {'transaction': transaction})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('transaction_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def manage_status(request):
    statuses = Status.objects.all()
    return render(request, 'core/manage_status.html', {'statuses': statuses})

@login_required
def manage_transaction_types(request):
    transaction_types = TransactionType.objects.all()
    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name')
        type_id = request.POST.get('type_id')

        if action == 'add':
            if name:
                TransactionType.objects.create(name=name)
                messages.success(request, 'Тип транзакции добавлен!')
            else:
                messages.error(request, 'Название не может быть пустым.')

        elif action == 'delete':
            type_obj = get_object_or_404(TransactionType, id=type_id)
            type_obj.delete()
            messages.success(request, 'Тип транзакции удалён!')

        return redirect('manage_transaction_types')

    return render(request, 'core/manage_transaction_types.html', {
        'transaction_types': transaction_types
    })

@login_required
def delete_transaction_type(request, type_id):
    type_obj = get_object_or_404(TransactionType, id=type_id)
    type_obj.delete()
    messages.success(request, 'Тип транзакции успешно удалён!')
    return redirect('manage_transaction_types')

@login_required
def manage_categories(request):
    categories = Category.objects.select_related('transaction_type').all()
    transaction_types = TransactionType.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name')
        transaction_type_id = request.POST.get('transaction_type_id')
        category_id = request.POST.get('category_id')

        if action == 'add':
            if name and transaction_type_id:
                Category.objects.create(name=name, transaction_type_id=transaction_type_id)
                messages.success(request, 'Категория добавлена!')
            else:
                messages.error(request, 'Заполните все поля.')

        elif action == 'delete':
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            messages.success(request, 'Категория удалена!')

        return redirect('manage_categories')

    return render(request, 'core/manage_categories.html', {
        'categories': categories,
        'transaction_types': transaction_types
    })
