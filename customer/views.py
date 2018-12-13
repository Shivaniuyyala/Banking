# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import *
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction
from customer.models import User
from account.models import CustomerAccountMapping, Account, Transaction, Beneficiary
from customer.forms import SignUpForm, AddBeneficiaryForm, TransferAmountForm
from decimal import Decimal
import datetime


from django.shortcuts import render


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        return super(SignUpView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customer:home')


def HomePage(request):
    if request.method == "GET":
        username = User.objects.filter(id=request.user.id).values_list('username')
        accounts = list(CustomerAccountMapping.objects.filter(customer=request.user.id).values_list(
            'account__ac_number'))
        if accounts:
            accounts = Account.objects.filter(ac_number__in=accounts[0])
        else:
            accounts = []
        return render(request, 'home.html', {"accounts": accounts, "username": username })


def TransactionHistory(request, ac_number=None):
    if request.method == "GET":
        transactions = Transaction.objects.filter(account__ac_number=ac_number)
        return render(request, 'view_transaction_history.html', {"transactions": transactions})


class AddBeneficiary(CreateView):
    template_name = 'add_beneficiary.html'

    def get_context_data(self, **kwargs):
        return super(AddBeneficiary, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        form = AddBeneficiaryForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = AddBeneficiaryForm(request.POST)
        import ipdb;ipdb.set_trace()
        name = str(request.POST.get('id_beneficiary_name'))
        ac_number = str(request.POST.get('id_account_number'))
        branch_code = str(request.POST.get('id_branch_code'))
        # account__branch = branch_code,
        if CustomerAccountMapping.objects.filter(customer__username=name, account=ac_number, status=True).exists():
            status, obj = Beneficiary.objects.get_or_create(user=request.user.id)
            beneficiary = CustomerAccountMapping.objects.get(customer__username=name, account=ac_number,
                                                             status=True).customer
            obj.beneficiary.add(beneficiary)
            obj.save()
            messages.success(request, "Beneficiary Added Successfully")
        else:
            messages.error(request, "Beneficiary Details are invalid, provide correct details !!!!!")

        return render(request, self.template_name, {"form": form})


class TransferAmountConfirm(CreateView):
    template_name = 'transfer_amount_confirm.html'

    def get_context_data(self, **kwargs):
        return super(TransferAmountConfirm, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        form = TransferAmountForm()
        if kwargs:
            beneficiary_id = int(kwargs['beneficiary_id'])
            ac_number, username = CustomerAccountMapping.objects.filter(id=beneficiary_id).values_list('account__ac_number',
                                                                              'customer__username')[0]

        return render(request, self.template_name, {"form": form, 'ac_number': ac_number, 'username':username })

    def post(self, request, *args, **kwargs):
        form = TransferAmountForm(request.POST)
        amount = Decimal(request.POST.get('amount'))
        if kwargs:
            beneficiary_id = int(kwargs['beneficiary_id'])
            beneficiary_ac_number = CustomerAccountMapping.objects.get(id=beneficiary_id).account.ac_number
            beneficiary = CustomerAccountMapping.objects.get(id=beneficiary_id).customer
            payee_ac_number = CustomerAccountMapping.objects.get(customer=request.user).account.ac_number
            TransferAmountConfirm.do_transaction(request.user, payee_ac_number, beneficiary, beneficiary_ac_number,
                                                 amount)
            messages.success(request, "Transaction completed Successfully")
            return HttpResponseRedirect('/')

    @classmethod
    def do_transaction(cls, payee, payee_ac_number, beneficiary, beneficiary_ac_number, amount):
        with transaction.atomic():
            payee_ac_number = Account.objects.select_for_update().get(ac_number=payee_ac_number)
            if payee_ac_number.balance < amount:
                raise "Insufficient Balance to complete the requested transaction"
            payee_ac_number.balance = payee_ac_number.balance-amount
            payee_ac_number.save()
            beneficiary_ac_number = Account.objects.select_for_update().get(ac_number=beneficiary_ac_number)
            beneficiary_ac_number.balance += amount
            beneficiary_ac_number.save()
            txn_id = 1111
            Transaction.objects.create(txn_id=txn_id, amount=amount, customer=payee, account=payee_ac_number,
                                       type=Transaction.DEBIT, txn_date=datetime.datetime.now())
            Transaction.objects.create(txn_id=txn_id, amount=amount, customer=beneficiary, account=beneficiary_ac_number,
                                       type=Transaction.CREDIT, txn_date=datetime.datetime.now())


def transferAmount(request):
    template_name = 'transfer_amount.html'
    if request.method == "GET":
        user = request.user
        beneficiary = Beneficiary.objects.filter(user=user)
        beneficiary_list = []
        if beneficiary:
            beneficiary_list = beneficiary[0].beneficiary.all()
        return render(request, template_name, {'beneficiary_list': beneficiary_list})

def interestCalculation(request):
    template_name = 'view_interest.html'
    interest_rate = 4
    if request.method == "GET":
        user = request.user
        obj = CustomerAccountMapping.objects.filter(customer=user)
        if obj:
            balance = obj[0].account.balance
            future_balance = round(balance+Decimal(balance*Decimal(0.04*12)),2)
            return render(request, template_name, {'balance':balance, 'future_balance': future_balance})















