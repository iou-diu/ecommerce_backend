# serializers.py
from rest_framework import serializers
from .models import Account, AccountHead, Transaction, TransactionLine

class AccountHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHead
        fields = ['id', 'name', 'head_type']

class AccountSerializer(serializers.ModelSerializer):
    account_head = AccountHeadSerializer()  # Nested serializer

    class Meta:
        model = Account
        fields = ['id', 'name', 'account_type', 'account_head']

class TransactionLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLine
        fields = ['id', 'account', 'transaction_type', 'amount']

class TransactionSerializer(serializers.ModelSerializer):
    lines = TransactionLineSerializer(many=True, required=False)

    class Meta:
        model = Transaction
        fields = ['id', 'head', 'description', 'lines']

    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        transaction = Transaction.objects.create(**validated_data)
        for line_data in lines_data:
            TransactionLine.objects.create(transaction=transaction, **line_data)
        return transaction

    def update(self, instance, validated_data):
        lines_data = validated_data.pop('lines', [])
        instance.head = validated_data.get('head', instance.head)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Update or create lines
        for line_data in lines_data:
            line_id = line_data.get('id', None)
            if line_id:
                line = TransactionLine.objects.get(id=line_id, transaction=instance)
                line.account = line_data.get('account', line.account)
                line.transaction_type = line_data.get('transaction_type', line.transaction_type)
                line.amount = line_data.get('amount', line.amount)
                line.save()
            else:
                TransactionLine.objects.create(transaction=instance, **line_data)

        return instance
