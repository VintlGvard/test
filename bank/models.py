from django.db import models
from django.contrib.auth.models import AbstractUser

class Client(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    cashback_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.username

class SavingsAccounts(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE, related_name="savings_accounts")
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Аккаунт {self.account_number}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Пополнение'),
        ('payment', 'Оплата')
    )
    account = models.ForeignKey(to=SavingsAccounts,on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.transaction_type == 'payment':
            cashback = float(self.amount)*0.01
            self.account.client.cashback_balance+=cashback
            self.account.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.transaction_type} {self.amount} on {self.timestamp} to {self.account}'
