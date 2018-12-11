# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from customer.models import BaseClass, User
from django.utils.translation import ugettext_lazy as _


class State(BaseClass):
    name = models.CharField(max_length=50, help_text='Enter the state name')

    def __unicode__(self):
        return u'%s' % self.name


class City(BaseClass):
    name = models.CharField(max_length=50, help_text='Enter the city')
    state = models.ForeignKey(State, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.name


class Branch(BaseClass):
    branch_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City)

    def __unicode__(self):
        return u'%s' % self.branch_code


class Account(BaseClass):
    ac_number = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    branch = models.ForeignKey(Branch)

    def __unicode__(self):
        return u'%s' % self.ac_number


class CustomerAccountMapping(BaseClass):
    customer = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s-%s' % (self.customer, self.account)


class Transaction(BaseClass):
    CREDIT = 1
    DEBIT = 2
    TRANSACTION_TYPES = (
        (CREDIT, 'credit'),
        (DEBIT, 'debit'),
    )

    txn_id = models.IntegerField(_("Transaction ID"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    customer = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    type = models.PositiveSmallIntegerField(choices=TRANSACTION_TYPES, default=1)

    def __unicode__(self):
        return u'%s' % self.txn_id

