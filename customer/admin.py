# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from customer.models import *


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'email', 'is_customer', 'is_active', 'is_staff', 'is_superuser', 'mobile_number',
                    'date_joined')


# class CustomerInfoAdmin(admin.ModelAdmin):
#     model = CustomerInfo
#     list_display = ('user', 'pan_number', 'aadhar_number')


admin.site.register(User, UserAdmin)
# admin.site.register(CustomerInfo, CustomerInfoAdmin)

