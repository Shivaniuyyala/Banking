# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import *
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from customer.models import User
from account.models import CustomerAccountMapping, Account, Transaction
from customer.models import Beneficiary
from customer.forms import SignUpForm, AddBeneficiaryForm, TransferAmountForm


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
        accounts = Account.objects.filter(ac_number__in=accounts[0])
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


class TransferAmount(CreateView):
    template_name = 'transfer_amount.html'

    def get_context_data(self, **kwargs):
        return super(TransferAmount, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        form = TransferAmountForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = TransferAmountForm(request.POST)
        return render(request, self.template_name, {"form": form})








