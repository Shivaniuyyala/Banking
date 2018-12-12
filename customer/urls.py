from django.conf.urls import include, url
from customer.views import *

urlpatterns = [

    url('customer/', include(([
        url('view_transaction_history/(?P<ac_number>\d+)/$', TransactionHistory, name='txn_history'),
        url('add_beneficiary/$', AddBeneficiary.as_view(), name='add_beneficiary'),
        url('transfer_amount/$', TransferAmount.as_view(), name='transfer_amount'),
    ], 'customer'), namespace='customer')),
]
