# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from customer.models import BaseClass, User
import datetime


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
    branch_code = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City)

    def __unicode__(self):
        return u'%s' % self.branch_code


class Account(BaseClass):
    ac_number = models.CharField(max_length=20, unique=True, primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    branch = models.ForeignKey(Branch, blank=True, null=True)
    ac_holder = models.ForeignKey(User)
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s-%s' % (self.ac_holder, self.ac_number)


class Transaction(BaseClass):
    CREDIT = 'credit'
    DEBIT = 'debit'
    TRANSACTION_TYPES = (
        (CREDIT, 'credit'),
        (DEBIT, 'debit'),
    )
    user = models.ForeignKey(User)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    from_account = models.ForeignKey(Account, related_name='payer_account')
    to_account = models.ForeignKey(Account, related_name='payee_account')
    type = models.CharField(choices=TRANSACTION_TYPES, default=CREDIT, max_length=50)
    txn_date = models.DateTimeField(editable=False, default=datetime.datetime.now)

    def __unicode__(self):
        return u'%s' % self.id


class BeneficiaryAccountDetails(BaseClass):
    user = models.ForeignKey(User)
    Beneficiary_account = models.ForeignKey(Account)
    transfer_limit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0),
                                                                                      MaxValueValidator(100000)],
                                         default=100000)

    def __unicode__(self):
        return u'%s' % self.user.username

