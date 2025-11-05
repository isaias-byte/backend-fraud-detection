from rest_framework import serializers
from .models import Transactions, TransactionsTest, UserInfo

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'  # Include all fields from the Transaction model
        # Alternatively, you can specify fields explicitly:
        # fields = ['id', 'distance_from_home', 'distance_from_last_transaction', 
        #           'ratio_to_median_purchase_price', 'repeat_retailer', 
        #           'used_chip', 'used_pin_number', 'online_order', 'fraud']

class TransactionTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionsTest
        fields = '__all__'  # Include all fields from the Transaction model
        # Alternatively, you can specify fields explicitly:
        # fields = ['id', 'distance_from_home', 'distance_from_last_transaction', 
        #           'ratio_to_median_purchase_price', 'repeat_retailer', 
        #           'used_chip', 'used_pin_number', 'online_order', 'fraud']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'  # Include all fields from the Transaction model
        # Alternatively, you can specify fields explicitly:
        # fields = ['id', 'name', 'card_bin', 'card_last_four', 
        #           'card_expiry_month', 'card_expiry_year']