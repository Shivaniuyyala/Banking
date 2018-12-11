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
    list_display = ('ac_number', 'branch', 'balance')


class CustomerAccountMappingAdmin(admin.ModelAdmin):
    model = CustomerAccountMapping
    list_display = ('customer', 'account', 'status')


class TransactionAdmin(admin.ModelAdmin):
    model = CustomerAccountMapping
    list_display = ('txn_id', 'amount', 'customer', 'account', 'type')


admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(CustomerAccountMapping, CustomerAccountMappingAdmin)
admin.site.register(Transaction, TransactionAdmin)
