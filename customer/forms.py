from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from customer.models import User


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', ]

    @transaction.atomic
    def save(self):
        user = super(SignUpForm, self).save(commit=False)
        user.is_customer = True
        user.save()
        return user


class AddBeneficiaryForm(forms.Form):
    beneficiary_name = forms.CharField(label=_('Beneficiary Name'), max_length=150, required=True)
    account_number = forms.CharField(required=True)
    branch_code = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(AddBeneficiaryForm, self).__init__(*args, **kwargs)


class TransferAmountForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(TransferAmountForm, self).__init__(*args, **kwargs)
