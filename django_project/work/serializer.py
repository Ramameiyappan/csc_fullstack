from rest_framework import serializers
from .models import Ledger
from login.models import User
from django.db import transaction
from .validators import validate_mobile_number
from decimal import Decimal

def get_balance(iscsc, operator, amount, commission):
    last = Ledger.objects.select_for_update().filter(operator=operator).order_by('-createdat').first()
    prev_bal = last.balance if last else 0
    if not iscsc:
        return prev_bal
    else:
        if prev_bal >= amount:
            return prev_bal - amount + commission
        else:
            raise serializers.ValidationError('balance is low first topup and proced')

class ElectricitySerializer(serializers.ModelSerializer):    
    class Meta:
        model = Ledger
        exclude = ['work_name', 'topup', 'balance', 'operator', 'createdat']

    def validate_account_no(self, value):
        if len(value)>8 and len(value)<13:
            return value
        else:
            raise serializers.ValidationError('enter the correct eb number')

    def create(self, validated_data):
        operator = self.context['request'].user
        with transaction.atomic():
            validated_data['balance'] = get_balance(validated_data['iscsc'], operator, validated_data['amount'], validated_data['commission'])
            validated_data['operator'] = operator
            validated_data['work_name'] = 'electricity'
            return super().create(validated_data)
    
class RechargeSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(
        validators=[validate_mobile_number])
    
    class Meta:
        model = Ledger
        exclude = ['work_name', 'account_no', 'topup', 'balance', 'operator', 'createdat']

    def validate_customer_name(self, value):
        brand_name = ('airtel', 'bsnl', 'jio', 'vi')
        if value and value.lower() in brand_name:
            return value
        else:
            raise serializers.ValidationError('mobile brand is not valid or not in our database')
        
    def create(self, validated_data):
        operator = self.context['request'].user
        with transaction.atomic():
            validated_data['balance'] = get_balance(validated_data['iscsc'], operator, validated_data['amount'], validated_data['commission'])
            validated_data['work_name'] = 'recharge'
            validated_data['account_no'] = validated_data['mobile']
            validated_data['operator'] = operator
            return super().create(validated_data)

class PanSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(
        validators=[validate_mobile_number])

    class Meta:
        model = Ledger
        exclude = ['work_name', 'amount', 'commission', 'topup', 'balance', 'operator', 'createdat']

    def validate_account_no(self, value):
        brand_name = ('uti', 'nsdl')
        if value and value.lower() in brand_name:
            return value
        else:
            raise serializers.ValidationError('provided name is not valid')
        
    def create(self, validated_data):
        operator = self.context['request'].user
        with transaction.atomic():
            validated_data['amount'] = Decimal('107')
            if validated_data['account_no'] == 'uti':
                validated_data['commission'] = Decimal('9.63')
            else:
                validated_data['commission'] = Decimal('9.37')
            validated_data['balance'] = get_balance(validated_data['iscsc'], operator, validated_data['amount'], validated_data['commission'])
            validated_data['work_name'] = 'pan'
            validated_data['operator'] = operator
            return super().create(validated_data)
    
class TravelSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(
        validators=[validate_mobile_number])
    
    class Meta:
        model = Ledger
        exclude = ['topup', 'balance', 'operator', 'createdat']

    def validate_work_name(self, value):
        travel = ('train', 'bus', 'flight')
        if value in travel:
            return value
        else:
            raise serializers.ValidationError('travel should be train, bus, flight')

    def create(self, validated_data):
        operator = self.context['request'].user
        with transaction.atomic():
            validated_data['balance'] = get_balance(validated_data['iscsc'], operator, validated_data['amount'], validated_data['commission'])
            validated_data['operator'] = operator
            return super().create(validated_data)
    
class InsuranceSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(
        validators=[validate_mobile_number])

    class Meta:
        model = Ledger
        exclude = ['topup', 'balance', 'operator', 'createdat']

    def validate_work_name(self, value):
        insurance_type = ('car', 'bike', 'health', 'crop')
        if value in insurance_type:
            return value
        else:
            raise serializers.ValidationError('insurance type is not in the database')

    def create(self, validated_data):
        operator = self.context['request'].user
        with transaction.atomic():
            validated_data['balance'] = get_balance(validated_data['iscsc'], operator, validated_data['amount'], validated_data['commission'])
            validated_data['operator'] = operator
            return super().create(validated_data)
    
class EsevaiSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(
        validators=[validate_mobile_number])

    class Meta:
        model = Ledger
        exclude = ['work_name', 'topup', 'balance', 'operator', 'createdat']

    def create(self, validated_data):
        operator = self.context['request'].user
        with transaction.atomic():
            validated_data['balance'] = get_balance(validated_data['iscsc'], operator, validated_data['amount'], validated_data['commission'])
            validated_data['work_name'] = 'esevai'
            validated_data['operator'] = operator
            return super().create(validated_data)
    
class OnlineSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(
        validators=[validate_mobile_number])
    
    class Meta:
        model = Ledger
        exclude = ['work_name', 'balance', 'topup', 'operator', 'createdat']

    def create(self, validated_data):
        operator = self.context['request'].user
        with transaction.atomic():
            validated_data['balance'] = get_balance(validated_data['iscsc'], operator, validated_data['amount'], validated_data['commission'])
            validated_data['work_name'] = 'online service'
            validated_data['operator'] = operator
            return super().create(validated_data)
    
class TopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        exclude = ['work_name','customer_name', 'account_no', 'mobile', 'commission', 'iscsc', 'balance', 'operator', 'createdat']
        
    def create(self, validated_data):
        operator = self.context['request'].user
        with transaction.atomic():
            last = Ledger.objects.select_for_update().filter(operator=operator).order_by('-createdat').first()
            prev_bal = last.balance if last else 0
            validated_data['work_name'] = 'topup'
            validated_data['customer_name'] = 'Na'
            validated_data['account_no'] = 'Na'
            validated_data['mobile'] = 'Na'
            validated_data['amount'] = 0
            validated_data['commission'] = 0
            validated_data['iscsc'] = True
            validated_data['balance'] = prev_bal + validated_data['topup']
            validated_data['operator'] = operator
            return super().create(validated_data)
        
class LedgerDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        exclude = ['operator']

class LedgerDashboardManagerSerializer(serializers.ModelSerializer):
    operator = serializers.CharField(source='operator.username')
    class Meta:
        model = Ledger
        fields = '__all__'

class UserDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'role']