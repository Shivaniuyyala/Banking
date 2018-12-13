from django.conf.urls import include, url
from customer.views import *

urlpatterns = [

    url('customer/', include(([
        url('view_transaction_history/(?P<ac_number>\d+)/$', TransactionHistory, name='txn_history'),
        url('add_beneficiary/$', AddBeneficiary.as_view(), name='add_beneficiary'),
        url('transfer_amount/$', transferAmount, name='transfer_amount'),
        url('transfer_amount_confirm/(?P<beneficiary_id>\d+)/$', TransferAmountConfirm.as_view(), name='txn_confirm'),
        url('calculate_interest/$', interestCalculation, name='calculate_interest'),
    ], 'customer'), namespace='customer')),
]
