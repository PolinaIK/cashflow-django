from django import forms
from .models import Transaction, Status, TransactionType, Category, SubCategory
from django.forms import DateInput

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'date': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class FilterForm(forms.Form):
    start_date = forms.DateField(label='С даты', required=False, widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='По дату', required=False, widget=DateInput(attrs={'type': 'date'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False, label='Статус')
    transaction_type = forms.ModelChoiceField(queryset=TransactionType.objects.all(), required=False, label='Тип')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Категория')
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(), required=False, label='Подкатегория')

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']
