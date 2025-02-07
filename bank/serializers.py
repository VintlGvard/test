from django.contrib.auth import authenticate
from .models import Client, SavingsAccounts, Transaction
from rest_framework import serializers
from django.db.models import Sum, Count

class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = Client
        fields = ('id', 'username', 'password', 'password2')

    def save(self, *args, **kwargs):
        user = Client(username=self.validated_data['username'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'detail': "Пароли не совпадают"})
        user.set_password(password)
        user.save()

        self.user = user
        return self.user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
    client: Client = None

    def validate(self, data):
        client = authenticate(**data)
        if client:
            return client
        return False

class SavingAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsAccounts
        fields = ('client', 'account_number', 'balance')

class TransactionsSerializer(serializers.ModelSerializer):
    total_transactions = serializers.SerializerMethodField()
    total_deposits = serializers.SerializerMethodField()
    total_payments = serializers.SerializerMethodField()
    transactions_count = serializers.SerializerMethodField()
    account = SavingAccountSerializer(read_only=True)
    cashback = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('id', 'transaction_type', 'account', 'amount', 'timestamp', 'total_transactions', 'transactions_count', 'total_payments', 'total_deposits', 'cashback')

    def get_transactions_count(self, obj):
        return obj.account.transactions.count()

    def get_total_deposits(self, obj):
        return obj.account.transactions.filter(transaction_type='deposit').aggregate(total=Sum('amount'))['total'] or 0

    def get_total_payments(self, obj):
        return obj.account.transactions.filter(transaction_type='payment').aggregate(total=Sum('amount'))['total'] or 0

    def get_cashback(self, obj):
        return float(obj.amount) * 0.01

    def get_total_transactions(self, obj):
        return self.get_total_deposits(obj) - self.get_total_payments(obj)