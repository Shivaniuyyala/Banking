# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from account.models import *


class StateAdmin(admin.ModelAdmin):
    model = State
    list_display = ('id', 'name')


class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ('id', 'name')


class BranchAdmin(admin.ModelAdmin):
    model = Branch
    list_display = ('branch_code', 'name', 'city')


class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ('ac_number', 'ac_holder', 'branch', 'balance', 'status')


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ('id', 'amount', 'from_account', 'to_account', 'type', 'txn_date')
    list_filter = ('txn_date', )


class BeneficiaryAccountDetailsAdmin(admin.ModelAdmin):
    model = BeneficiaryAccountDetails
    list_display = ('user', 'Beneficiary_account', 'transfer_limit')


admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(BeneficiaryAccountDetails, BeneficiaryAccountDetailsAdmin)

