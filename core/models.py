from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TransactionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"{self.transaction_type.name} → {self.name}"

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.category.name} → {self.name}"

class Transaction(models.Model):
    date = models.DateField(verbose_name="Дата", auto_now_add=False)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} | {self.transaction_type.name} | {self.amount} р."
