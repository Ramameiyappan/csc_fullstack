from django.db import models
from login.models import User

class Ledger(models.Model):
    work = [
        ('electricity', 'Electricity'),
        ('recharge', 'Recharge'),
        ('pan', 'PAN'),
        ('train', 'Train'),
        ('bus', 'Bus'),
        ('flight','Flight'),
        ('car','Car'),
        ('bike','Bike'),
        ('health','Health'),
        ('crop', 'Crop'),
        ('topup', 'Topup'),
        ('esevai', 'Esevai'),
        ('other_work','Other' )
    ]

    work_name = models.CharField(choices=work, max_length=20)
    customer_name = models.CharField(null=False, max_length=20)
    account_no = models.CharField(null=False, max_length=25)
    mobile = models.CharField(null=True, max_length=10)
    amount = models.DecimalField(null=False, default=0, max_digits=7, decimal_places=2)
    commission = models.DecimalField(null=False, default=0, max_digits=6, decimal_places=2)
    topup = models.DecimalField(null=True, max_digits=7, decimal_places=2)
    iscsc = models.BooleanField(null=False, default=1)
    balance = models.DecimalField(default=0,max_digits=7, decimal_places=2)
    operator = models.ForeignKey(User, on_delete=models.PROTECT)
    createdat = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Ledger'