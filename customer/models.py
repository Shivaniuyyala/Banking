# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
import datetime


class User(AbstractUser):
    is_customer = models.BooleanField(blank=True, default=False)
    mobile_number = models.CharField(_("Mobile Number"), max_length=15)
    # pan_number = models.CharField(_("PAN Number"), max_length=20)
    # aadhar_number = models.CharField(_("Aadhar Number"), max_length=4)

    def __unicode__(self):
        return u'%s' % self.username


class BaseClass(models.Model):
    created_on = models.DateTimeField(editable=False, default=datetime.datetime.now)
    updated_on = models.DateTimeField(editable=False,  auto_now=True)
    created_by = models.ForeignKey(User, editable=False, blank=True, null=True,
                                   related_name="%(class)s_created_by")
    updated_by = models.ForeignKey(User, editable=False, blank=True, null=True,
                                   related_name="%(class)s_updated_by")

    class Meta:
        abstract = True

    @classmethod
    def table_name(cls):
        return cls._meta.db_table


# class CustomerInfo(BaseClass):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     pan_number = models.CharField(_("PAN Number"), max_length=20)
#     aadhar_number = models.CharField(_("Aadhar Number"), max_length=40)
#
#     def __unicode__(self):
#         return u'%s' % self.user.username





