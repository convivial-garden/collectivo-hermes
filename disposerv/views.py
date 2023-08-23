from django.http import HttpResponse, JsonResponse
import logging
import json
from django.db.models import Q
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
import datetime
import pytz
import logging
import requests
from collectivo.utils.mixins import HistoryMixin, SchemaMixin
from collectivo.utils.permissions import (
    IsAuthenticated,
    IsSuperuser,
    ReadOrIsSuperuser,
)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

from rest_framework import viewsets, generics
from .models import \
    PositionAddress, \
    Customer, \
    ContractPosition, \
    RepeatedContract, \
    Street, \
    Contract, \
    Dispo, \
    TimesRecord, \
    Staff, \
    Settings
from .serializers import \
    AddressSerializer, \
    CustomerSerializer, \
    ContractPositionSerializer, \
    ContractGetSerializer, \
    StreetSerializer, \
    ContractSerializer, \
    ArchiveContractSerializer, \
    DispoSerializer, \
    TimesRecordSerializer, \
    StaffSerializer, \
    StaffNamesSerializer, \
    DelayedPaymentSerializer, \
    FullTimesRecordSerializer, \
    SettingsSerializer

#
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
    permission_classes = [IsSuperuser]



class AddressViewSet(HistoryMixin, SchemaMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = PositionAddress.objects.all().order_by('street')
    serializer_class = AddressSerializer
    permission_classes = [IsSuperuser]


class DispoViewSet(HistoryMixin, SchemaMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Dispo.objects.all().order_by('id')
    serializer_class = DispoSerializer
    permission_classes = [IsSuperuser]


class TimesRecordViewSet(HistoryMixin, SchemaMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = TimesRecord.objects.all().order_by('id')
    serializer_class = TimesRecordSerializer
    permission_classes = [IsSuperuser]


class StaffViewSet(HistoryMixin, SchemaMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Staff.objects.all().order_by('user__id')
    serializer_class = StaffSerializer
    permission_classes = [IsSuperuser]


class StreetViewSet(HistoryMixin, SchemaMixin, generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = StreetSerializer
    permission_classes = [IsSuperuser]

    def get_queryset(self):
        name = self.kwargs.get('name', '')
        result = Street.objects.all()
        settings = Settings.objects.first()

        if (name != ''):
            try:
                result = result.filter(name__istartswith=name.split(' ')[0])
                checked_for_a_number = False
                for part in name.split(' '):
                    result = result.filter(name__icontains=part)
                    if (is_number(part) and (not checked_for_a_number)):
                        result = result.filter(nr_von__exact=part)
                        checked_for_a_number = True
            except:
                print("ERROR")
        return result.distinct()

class DelayedPaymentView(HistoryMixin, SchemaMixin, generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = CustomerSerializer
    permission_classes = [IsSuperuser]

    def get_queryset(self):
        return Customer.objects.filter(has_delayed_payment__exact=True).distinct().order_by('id')

class ContractViewSet(HistoryMixin, SchemaMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Contract.objects.all().order_by('id')
    def get_serializer_class(self):
        print(self.action)
        return ContractSerializer
    permission_classes = [IsSuperuser]


def fastStreets(request, **kwargs):
    name = kwargs.get('name', '')
    results = []
    print("fastStreets", name)
    if (name != '' and len(name) > 3):
        try:
            name_split = name.split(' ')
            result = Street.objects.filter(name__istartswith=name_split[0])
            for part in name_split:
                if (is_number(part)):
                    result = result.filter(nr_von__iexact=part)
                else:
                    result = result.filter(name__icontains=part)
            result = result.distinct()
        except:
            print("ERROR")

        if (len(result) == 0):
                try:
                    here_maps_api_key = "Up_vTCjQcg2_WoQK79Dlzj6a_MMliPdfYhO0Cvn3kf4"
                    settings = Settings.objects.first()
                    if (here_maps_api_key == ''):
                            print("ERROR: no here maps api key")
                    else:
                            if (name != ''):
                                print("faststreets: get streets from here maps")
                                url = "https://geocode.search.hereapi.com/v1/geocode?at="+str(settings.gps_lat)+","+str(settings.gps_lon)+"&q="+name+" "+settings.city+"&lang=de&limit=5&apiKey="+here_maps_api_key
                                print(url)
                                data = requests.get(url)
                                items = data.json()['items']
                                for element in items:
                                    # print(element)
                                    if element['resultType'] == 'street' and element['distance']<50000:
                                        print("street")
                                        name = element['address']['street']
                                        postal_code = "0000"
                                        if 'postalCode' in element['address']:
                                            postal_code = element['address']['postalCode']

                                        street = Street.objects.update_or_create(name=name,name_street=name, 
                                                                       nr_von=0, 
                                                                       nr_bis=0, 
                                                                       postal_code=postal_code,
                                                                       lat= element['position']['lat'],
                                                                         lon= element['position']['lng'],  )
                                        results.append({"value": str(len(results)), "label": element["title"], "data": street})
                except Exception as error:
                    print("ERROR: failed to query here maps", error)
        else:
            for (index, res) in enumerate(result.values()):
                results.append({"value": str(index), "label": res['name']+" "+res['postal_code'], "data": res})
    return JsonResponse(results, safe=False)


def totalSales(request, **kwargs):
    year = kwargs['year']
    month = kwargs['month']
    day = kwargs['day']
    contracts = Contract.objects \
        .filter(positions__start_time__year=year,
                positions__start_time__month=month,
                positions__start_time__day=day,
                positions__dispo__preliminary=False,
                ) \
        .distinct().order_by('id')
    price = 0.
    for contract in contracts:
        price += float(contract.price)
    resp = {'totalPrice' : price}
    return JsonResponse(resp)

def totalContracts(request):
    numberOfContracts = len(Contract.objects.filter(positions__dispo__preliminary=False, repeated__isnull=True).distinct())
    return JsonResponse({'numberOfContracts' : numberOfContracts})

def getAnon(request):
    anon = Customer.objects.filter(name__exact="_anon").distinct().order_by('id')
    if (len(anon) == 0):
        anon = Customer.objects.create(name = "_anon")
        return JsonResponse({"error" : 'created anon', 'id' : anon.id})
    else:
        return JsonResponse({'id': anon[0].id})

class DelayedPaymentViewSet(HistoryMixin, SchemaMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = DelayedPaymentSerializer
    permission_classes = [IsSuperuser]


class CustomersByNameList(HistoryMixin, SchemaMixin, generics.ListAPIView):
    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsSuperuser]

    def get_queryset(self):
        name = self.kwargs['name']
        if len(name)>2:
            return Customer.objects.filter(name__icontains=name).distinct()
        return []

class CustomersByExternalIdList(HistoryMixin, SchemaMixin, generics.ListAPIView):
    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsSuperuser]

    def get_queryset(self):
        id = self.kwargs['id']
        return Customer.objects.filter(external_id__icontains=id).distinct()

class StaffByDateList(HistoryMixin, SchemaMixin, generics.ListAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsSuperuser]
    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        now = timezone.now().replace(tzinfo=pytz.UTC)
        staff =  Staff.objects \
            .filter(times__start_datetime__year=year,
                    times__start_datetime__month=month,
                    times__start_datetime__day=day) \
            .distinct().order_by('user')
        return staff

class ActiveStaffByDateList(HistoryMixin, SchemaMixin, generics.ListAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsSuperuser]
    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        now = timezone.now()
        now = timezone.now().replace(tzinfo=pytz.UTC)
        staff = Staff.objects \
            .filter(times__start_datetime__year=year,
                    times__start_datetime__month=month,
                    times__start_datetime__day=day) \
            .filter(Q(times__end_datetime__gt = now)
                    | Q(times__start_datetime__day = day,
                        times__start_datetime__month=month,
                        times__start_datetime__year=year,
                        times__end_datetime__isnull = True)) \
            .distinct().order_by('user')
        print(staff)
        return staff

class TimesByDateList(HistoryMixin, SchemaMixin, generics.ListAPIView):
    serializer_class = FullTimesRecordSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsSuperuser]
    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        return TimesRecord.objects \
            .filter(start_datetime__year=year,
                    start_datetime__month=month,
                    start_datetime__day=day) \
            .distinct().order_by('id')

class StaffNames(HistoryMixin, SchemaMixin, generics.ListAPIView):
    serializer_class = StaffNamesSerializer
    permission_classes = [IsSuperuser]
    staff = Staff.objects.all().order_by('user__first_name')
    if (len(staff) == 0):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.all()
        print(users)
        for user in users:
            print(user)
            staff = Staff.objects.create(user=user)
            staff.save()
    queryset = staff

class ContractsArchiveList(HistoryMixin, SchemaMixin, generics.ListAPIView):
    serializer_class = ArchiveContractSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsSuperuser]
    def get_queryset(self):
        """
        View returns all contracts except if theres a date parameter in the url
        :return:
        """
        year = self.kwargs.get('year', '')
        month = self.kwargs.get('month', '')
        day = self.kwargs.get('day', '')
        riderId = self.kwargs.get('riderid', '')
        customerId = self.kwargs.get('customerid', '')

        archive_kwargs = {}
        if (year != ''):
            archive_kwargs['positions__start_time__year'] = year
        if (month != ''):
            archive_kwargs['positions__start_time__month'] = month
        if (day != ''):
            archive_kwargs['positions__start_time__day'] = day
        if (riderId != ''):
            archive_kwargs['positions__dispo__dispatched_to__id'] = riderId
        if (customerId != ''):
            archive_kwargs['positions__customer__id'] = customerId


        assigned_contracts_ids = Contract.objects.filter(positions__position__gte=1, positions__dispo__isnull=False).distinct().order_by('id')

        response = Contract.objects \
            .filter(id__in=assigned_contracts_ids, **archive_kwargs)\
            .distinct().order_by('id')
        response.order_by('-positions__dispo__created')
        return response

class PreordersList(HistoryMixin, SchemaMixin, generics.ListAPIView):
    def get_serializer_class(self):
        print(self)
        return ContractSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsSuperuser]

    def get_queryset(self):
        """
        View returns all contracts except if theres a date parameter in the url
        :return:
        """
        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        tomorrow = tomorrow.replace(tzinfo=pytz.UTC)
        archive_kwargs = {}
        archive_kwargs['positions__start_time__gt'] = tomorrow
        archive_kwargs['fromrepeated'] = False

        return Contract.objects \
            .filter(**archive_kwargs) \
            .distinct().order_by('id')


class ContractsByDateList(HistoryMixin, SchemaMixin, generics.ListAPIView):
    def get_serializer_class(self):
        return ContractGetSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsSuperuser]
    def get_queryset(self):
        """
        View returns all contracts except if theres a date parameter in the url
        :return:
        """

        year = self.kwargs.get('year', '')
        month = self.kwargs.get('month', '')
        day = self.kwargs.get('day', '')
        rider_id = self.kwargs.get('rider', -1)
        if (rider_id == "-2"):
            print("get all contracts")
            return Contract.objects \
                .filter(positions__start_time__year=year,
                        positions__start_time__month=month,
                        positions__start_time__day=day,
                        # repeated__isnull=True
                        ) \
                .distinct().order_by('id')
        elif (rider_id != -1):
            return Contract.objects \
                .filter(positions__start_time__year=year,
                        positions__start_time__month=month,
                        positions__start_time__day=day,
                        positions__dispo__dispatched_to__user=rider_id,
                        positions__dispo__preliminary=False,
                        #repeated__isnull=True
                        ) \
                .order_by('id') \
                .distinct()
        else:
            return Contract.objects\
                .filter(positions__start_time__year=year,
                        positions__start_time__month=month,
                        positions__start_time__day=day,
                        #repeated__isnull=True
                        ) \
                .exclude(Q(positions__dispo__preliminary=False)) \
                .distinct().order_by('id')

class ContractsSelfByDateList(ContractsByDateList):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        View returns all contracts except if theres a date parameter in the url
        :return:
        """

        year = self.kwargs.get('year', '')
        month = self.kwargs.get('month', '')
        day = self.kwargs.get('day', '')
        rider_id = self.request.user.id
        return Contract.objects \
            .filter(positions__start_time__year=year,
                    positions__start_time__month=month,
                    positions__start_time__day=day,
                    positions__dispo__dispatched_to__id=rider_id,
                    positions__dispo__preliminary=False,
                    #repeated__isnull=True
                    ) \
            .order_by('id') \
            .distinct()
class RepeatedContracts(HistoryMixin, SchemaMixin, generics.ListAPIView):
    serializer_class = ContractSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsSuperuser]

    def get_queryset(self):
        weekday = self.kwargs.get('weekday', '')
        return RepeatedContract.objects \
            .filter((Q(repeated__end_date__gte=timezone.now()) | Q(repeated__end_date__isnull=True)),
                    repeated__days_of_the_week__icontains=weekday) \
            .distinct().order_by('id')

class TerminatedRepeatedContracts(HistoryMixin, SchemaMixin, generics.ListAPIView):
    serializer_class = ContractSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsSuperuser]

    def get_queryset(self):
        weekday = self.kwargs.get('weekday', '')
        return Contract.objects \
            .filter(repeated__end_date__isnull=False,
                    repeated__end_date__lt=timezone.now(),
                    repeated__days_of_the_week__icontains=weekday) \
            .distinct().order_by('id')

class ContractPositionViewSet(HistoryMixin, SchemaMixin, viewsets.ModelViewSet):
    queryset = ContractPosition.objects.all().order_by('start_time')
    pagination_class = StandardResultsSetPagination
    serializer_class = ContractPositionSerializer
    permission_classes = [IsSuperuser]


class CustomerViewSet(HistoryMixin, SchemaMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('name')
    pagination_class = StandardResultsSetPagination
    serializer_class = CustomerSerializer
    permission_classes = [IsSuperuser]


class SettingsViewSet(HistoryMixin, SchemaMixin, viewsets.ModelViewSet):
    queryset = Settings.objects.all().order_by('id')
    if (len(queryset) == 0):
        print("disposerv: create settings")
        Settings.objects.create()
        queryset = Settings.objects.all().order_by('id')
    
    serializer_class = SettingsSerializer
    permission_classes = [IsSuperuser]
