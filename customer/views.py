# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import *
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction
from customer.models import User
from account.models import *
from customer.forms import SignUpForm, AddBeneficiaryForm, TransferAmountForm
from account.decorators import login_required
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
        ac_number = int(self.request.POST.get('ac_number'))
        obj, status = Account.objects.get_or_create(ac_number=ac_number, ac_holder=user)
        obj.status = True
        obj.save()
        login(self.request, user)
        return redirect('home')


@login_required
def HomePage(request):
    if request.method == "GET":
        username = request.user.username
        accounts = Account.objects.filter(ac_holder=request.user.id)
        return render(request, 'home.html', {"accounts": accounts, "username": username})


@login_required
def TransactionHistory(request, ac_number=None):
    if request.method == "GET":
        transactions = Transaction.objects.filter(user=request.user)
        return render(request, 'view_transaction_history.html', {"transactions": transactions})


class AddBeneficiary(CreateView):
    template_name = 'add_beneficiary.html'

    @login_required
    def get_context_data(self, **kwargs):
        return super(AddBeneficiary, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        form = AddBeneficiaryForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = AddBeneficiaryForm(request.POST)
        name = str(request.POST.get('beneficiary_name'))
        ac_number = str(request.POST.get('account_number'))
        # branch_code = str(request.POST.get('id_branch_code'))
        transfer_limit = Decimal(request.POST.get('transfer_limit'))
        if Account.objects.filter(ac_holder__username=name, ac_number=ac_number, status=True).exists():
            obj, status = BeneficiaryAccountDetails.objects.get_or_create(user=request.user,
                                                                          Beneficiary_account_id=ac_number)
            if status:
                obj.transfer_limit = transfer_limit
                obj.save()
                messages.success(request, "Beneficiary Added Successfully")
            else:
                messages.info(request, "Beneficiary already Exist with given details")
        else:
            messages.error(request, "Beneficiary Details are invalid, provide correct details !!!!!")

        return render(request, self.template_name, {"form": form})


class TransferAmountConfirm(CreateView):
    template_name = 'transfer_amount_confirm.html'

    @login_required
    def get_context_data(self, **kwargs):
        return super(TransferAmountConfirm, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        form = TransferAmountForm()
        if kwargs:
            ac_number = int(kwargs['ac_number'])
            ac_number, username = Account.objects.filter(ac_number=ac_number).values_list('ac_number',
                                                                              'ac_holder__username')[0]

        return render(request, self.template_name, {"form": form, 'ac_number': ac_number, 'username':username })

    def post(self, request, *args, **kwargs):
        form = TransferAmountForm(request.POST)
        amount = Decimal(request.POST.get('amount'))
        if kwargs:
            payee_ac_number = int(kwargs['ac_number'])
            payee = Account.objects.get(ac_number=payee_ac_number).ac_holder
            payer_ac_number = Account.objects.get(ac_holder=request.user).ac_number
            transfer_limit = BeneficiaryAccountDetails.objects.get(user=request.user,
                                                                 Beneficiary_account_id=payee_ac_number).transfer_limit
            if transfer_limit < amount:
                messages.error(request, "Beneficiary Transfer Limit exceeded")
                return render(request, self.template_name, {"form": form, 'ac_number': payee_ac_number, 'username': payee})
            TransferAmountConfirm.do_transaction(request.user, payer_ac_number, payee, payee_ac_number, amount)
            messages.success(request, "Transaction completed Successfully")
            return HttpResponseRedirect('/')

    @classmethod
    def do_transaction(cls, payer, payer_ac_number, payee, payee_ac_number, amount):
        with transaction.atomic():
            payer_ac = Account.objects.select_for_update().get(ac_number=payer_ac_number)
            if payer_ac.balance < amount:
                raise  ValidationError("Insufficient Balance to complete the requested transaction")
            payer_ac.balance = payer_ac.balance-amount
            payer_ac.save()
            payee_ac = Account.objects.select_for_update().get(ac_number=payee_ac_number)
            payee_ac.balance += amount
            payee_ac.save()
            Transaction.objects.create(user=payer, amount=amount, from_account=payer_ac, to_account=payee_ac,
                                       type=Transaction.DEBIT, txn_date=datetime.datetime.now())
            Transaction.objects.create(user=payee, amount=amount, from_account=payer_ac, to_account=payee_ac,
                                       type=Transaction.CREDIT, txn_date=datetime.datetime.now())


@login_required
def transferAmount(request):
    template_name = 'transfer_amount.html'
    if request.method == "GET":
        user = request.user
        beneficiary_list = list(BeneficiaryAccountDetails.objects.filter(user=user))
        return render(request, template_name, {'beneficiary_list': beneficiary_list})

@login_required
def interestCalculation(request):
    template_name = 'view_interest.html'
    interest_rate = 4
    if request.method == "GET":
        user = request.user
        obj = Account.objects.filter(ac_holder=user)
        if obj:
            balance = obj[0].balance
            future_balance = round(balance+Decimal(balance*Decimal(0.04*12)),2)
            return render(request, template_name, {'balance':balance, 'future_balance': future_balance})















