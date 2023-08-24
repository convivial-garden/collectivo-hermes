"""hermesdisposerver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r'addresses', views.AddressViewSet)
router.register(r'positions', views.ContractPositionViewSet)
router.register(r'contracts', views.ContractViewSet)
router.register(r'staff', views.StaffViewSet)
router.register(r'timesrecord', views.TimesRecordViewSet)
router.register(r'dispo', views.DispoViewSet)
router.register(r'delayedpayment', views.DelayedPaymentViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'settings', views.SettingsViewSet)



urlpatterns = [
    re_path(r'^api/hermes/disposerv/street/name/(?P<name>.+)/(?P<nr>.+)/$', views.StreetViewSet.as_view()),
    re_path(r'^api/hermes/disposerv/street/name/(?P<name>.+)/$', views.StreetViewSet.as_view()),
    re_path(r'^api/hermes/disposerv/faststreet/name/(?P<name>.+)/$', views.fastStreets),
    re_path(r'^api/hermes/disposerv/', include(router.urls)),
    re_path(r'^api/hermes/disposerv/contracts/date/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/$', views.ContractsByDateList.as_view()),
    re_path(r'^api/hermes/disposerv/contracts/customer/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/(?P<customerid>.+)/$', views.ContractsArchiveList.as_view()),
    re_path(r'^api/hermes/disposerv/contracts/customer/(?P<year>.+)/(?P<month>.+)/(?P<customerid>.+)/$', views.ContractsArchiveList.as_view()),
    re_path(r'^api/hermes/disposerv/contracts/customer/(?P<year>.+)/(?P<customerid>.+)/$', views.ContractsArchiveList.as_view()),
    re_path(r'^api/hermes/disposerv/contracts/archive/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/(?P<riderid>.+)/(?P<customerid>.+)/$', views.ContractsArchiveList.as_view()),
    re_path(r'^api/hermes/disposerv/contracts/archive/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/(?P<riderid>.+)/$', views.ContractsArchiveList.as_view()),
    re_path(r'^api/hermes/disposerv/contracts/archive/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/$', views.ContractsArchiveList.as_view()),
    re_path(r'^api/hermes/disposerv/contracts/archive/(?P<year>.+)/(?P<month>.+)/$', views.ContractsArchiveList.as_view()),
    re_path(r'^api/hermes/disposerv/contracts/archive/(?P<year>.+)/$', views.ContractsArchiveList.as_view()),
    re_path(r'^api/hermes/disposerv/contracts/repeated/(?P<id>.+)/$', views.RepeatedContracts.as_view()),
    re_path(r'^api/hermes/disposerv/preorders/$', views.PreordersList.as_view()),
    re_path(r'^api/hermes/disposerv/payments/$', views.DelayedPaymentView.as_view()),
    re_path(r'^api/hermes/disposerv/anon/$', views.getAnon),
    re_path(r'^api/hermes/disposerv/contracts/rider/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/(?P<rider>.+)/$', views.ContractsByDateList.as_view()),
    re_path(r'^api/hermes/disposerv/contracts/rider/self/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/$', views.ContractsSelfByDateList.as_view()),
    re_path(r'^api/hermes/disposerv/repeatedall', views.RepeatedContracts.as_view()),
    re_path(r'^api/hermes/disposerv/repeated/(?P<weekday>.+)/$', views.RepeatedContracts.as_view()),
    re_path(r'^api/hermes/disposerv/repeateddoneall', views.TerminatedRepeatedContracts.as_view()),
    re_path(r'^api/hermes/disposerv/repeateddone/(?P<weekday>.+)/$', views.TerminatedRepeatedContracts.as_view()),
    re_path(r'^api/hermes/disposerv/staff/date/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/$', views.StaffByDateList.as_view()),
    re_path(r'^api/hermes/disposerv/staff/active/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/$', views.ActiveStaffByDateList.as_view()),
    re_path(r'^api/hermes/disposerv/times/date/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/$', views.TimesByDateList.as_view()),
    re_path(r'^api/hermes/disposerv/times/date/(?P<year>.+)/(?P<month>.+)/$', views. TimesByMonthList.as_view()),
    re_path(r'^api/hermes/disposerv/staffnames/$', views.StaffNames.as_view()),
    re_path(r'^api/hermes/disposerv/sales/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/$', views.totalSales),
    re_path(r'^api/hermes/disposerv/totalcontracts/$', views.totalContracts),
    re_path(r'^api/hermes/disposerv/customers/name/(?P<name>.+)/$', views.CustomersByNameList.as_view()),
    re_path(r'^api/hermes/disposerv/customers/externalid/(?P<id>.+)/$', views.CustomersByExternalIdList.as_view()),
]
