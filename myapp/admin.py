from django.contrib import admin
from .models import Transactions, TransactionsTest, UserInfo

# Register your models here.

admin.site.register(Transactions)
admin.site.register(TransactionsTest)
admin.site.register(UserInfo)