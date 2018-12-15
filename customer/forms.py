from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from customer.models import User


class SignUpForm(UserCreationForm):
    ac_number = forms.CharField(label="Account Number", max_length=20, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'ac_number']

    @transaction.atomic
    def save(self):
        user = super(SignUpForm, self).save(commit=False)
        user.is_customer = True
        user.save()
        return user


class AddBeneficiaryForm(forms.Form):
    beneficiary_name = forms.CharField(label=_('Beneficiary Name'), max_length=50, required=True)
    account_number = forms.CharField(required=True)
    # branch_code = forms.CharField(required=True)
    transfer_limit = forms.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(100000)])

    def __init__(self, *args, **kwargs):
        super(AddBeneficiaryForm, self).__init__(*args, **kwargs)


class TransferAmountForm(forms.Form):
    amount = forms.DecimalField(required=True)

    def __init__(self, *args, **kwargs):
        super(TransferAmountForm, self).__init__(*args, **kwargs)
