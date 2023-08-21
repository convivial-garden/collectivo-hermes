from rest_framework import serializers
import requests
from .models import \
    Address, \
    Customer, \
    ContractPosition, \
    Street, \
    Contract, \
    Dispo, \
    TimesRecord, \
    Staff, \
    Repeated, \
    Settings, \
    StreetWithNumber

from collectivo.utils.serializers import UserFields, UserIsPk

def create_new_position(validated_data, **kwargs):
    contract = kwargs.get('contract', 'null')
    address_data = validated_data.pop('address')
    customer = validated_data.pop('new_customer')

    position = ContractPosition.objects.create(**validated_data, contract = contract, customer = customer)

    address = address_data[0]
    address.pop('position', 'null')
    # set lat and lon
    streetWithNumber = StreetWithNumber.objects.filter(name=address.get('street'), nr=address.get('number'), postal_code=address.get('postal_code'))
    if (streetWithNumber):
        position.lat = streetWithNumber[0].lat
        position.lon = streetWithNumber[0].lon
    else:
        here_maps_api_key = "Up_vTCjQcg2_WoQK79Dlzj6a_MMliPdfYhO0Cvn3kf4"
        settings = Settings.objects.first()
        if (here_maps_api_key == ''):
                print("ERROR: no here maps api key")
        else:
            print("get streets from here maps")
            url = "https://geocode.search.hereapi.com/v1/geocode?at="+str(settings.gps_lat)+","+str(settings.gps_lon)+"&q="+address.get('street')+" "+address.get('number')+" "+address.get('postal_code')+"&lang=de&limit=5&apiKey="+here_maps_api_key
            print(url)
            data = requests.get(url)
            items = data.json()['items']
            if (len(items) > 0):
                position.lat = items[0]['position']['lat']
                position.lon = items[0]['position']['lng']
                StreetWithNumber.objects.create(name=address.get('street'), nr=address.get('number'), postal_code=address.get('postal_code'), lat=position.lat, lon=position.lon)
    Address.objects.create(**address, position=position)
    return position

def create_new_repeated(validated_data, **kwargs):
    try:
        contract = kwargs.get('contract', None)
        repeated = Repeated.objects.create(**validated_data, contract = contract)
        return repeated
    except TypeError:
        return None

def update_instance_address(instance_address, address_data):
    instance_address.street = address_data.get('street', instance_address.street)
    instance_address.number = address_data.get('number', instance_address.number)
    instance_address.stair = address_data.get('stair', instance_address.stair)
    instance_address.level = address_data.get('level', instance_address.level)
    instance_address.door = address_data.get('door', instance_address.door)
    instance_address.extra = address_data.get('extra', instance_address.extra)
    instance_address.postal_code = address_data.get('postal_code', instance_address.postal_code)
    instance_address.lat = address_data.get('lat', instance_address.lat)
    instance_address.lon = address_data.get('lon', instance_address.lon)
    return instance_address

def update_position_instance(instance, validated_data):
    instance.customer = validated_data.get('new_customer', instance.customer)
    instance.anon_name = validated_data.get('anon_name', instance.anon_name)
    instance.position = validated_data.get('position', instance.position)
    instance.start_mode = validated_data.get('start_mode', instance.start_mode)
    instance.start_time = validated_data.get('start_time', instance.start_time)
    instance.memo = validated_data.get('memo', instance.memo)
    instance.weight_size_bonus = validated_data.get('weight_size_bonus', instance.weight_size_bonus)
    instance.is_express = validated_data.get('is_express', instance.is_express)
    instance.is_cargo = validated_data.get('is_cargo', instance.is_cargo)
    instance.is_bigbuilding = validated_data.get('is_bigbuilding', instance.is_bigbuilding)
    instance.get_there_bonus = validated_data.get('get_there_bonus', instance.get_there_bonus)
    instance.waiting_bonus = validated_data.get('waiting_bonus', instance.waiting_bonus)
    instance.distance = validated_data.get('distance', instance.distance)
    instance.zone = validated_data.get('zone', instance.zone)
    instance.bonus = validated_data.get('bonus', instance.bonus)
    instance.price = validated_data.get('price', instance.price)
    instance.phone_1 = validated_data.get('phone_1', instance.phone_1)
    instance.email = validated_data.get('email', instance.email)
    instance.talk_to = validated_data.get('talk_to', instance.talk_to)

    return instance

def update_position(instance, validated_data):
    try:
        address = validated_data.pop("address")
        address_data = address[0]
        for instance_address in instance.address.all():
            instance_address = update_instance_address(instance_address, address_data)
            instance_address.save()
    except IndexError:
        pass
        # update position
    instance = update_position_instance(instance, validated_data)
    return instance

def update_repeated(instance, validated_data):
    try:
        validated_data = validated_data.get('repeated')
        if (validated_data):
            instance.start_date = validated_data.get('start_date', instance.start_date)
            instance.end_date = validated_data.get('end_date', instance.end_date)
            instance.days_of_the_week = validated_data.get('days_of_the_week', instance.days_of_the_week)
            instance.save()
        else:
            instance.delete()
            return None
    except IndexError:
        pass
    return instance

class DispoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispo
        fields = ('url', 'created', 'contract', 'dispatched_to', 'sequence', 'position', 'preliminary')
class StaffNamesSerializer(UserIsPk, UserFields):
    # id = serializers.IntegerField()
    # name = serializers.CharField()
    # url = serializers.HyperlinkedRelatedField(view_name='staff-detail', read_only=True)

    # get name from user
    # user_name = serializers.SerializerMethodField('get_user_name')
    class Meta:
        model = Staff
        # get name from user
        fields = "__all__"
    # def get_user_name(self, obj):
    #     print(obj)
    #     return obj.user.username


class TimesRecordSerializer(serializers.HyperlinkedModelSerializer):
    staff_member = StaffNamesSerializer(read_only=True)
    class Meta:
        model = TimesRecord
        fields = ('id', 'url', 'date', 'start_datetime', 'end_datetime', 'mode', 'staff_member')


class StaffSerializer(UserIsPk, UserFields, serializers.ModelSerializer):
    times = TimesRecordSerializer(many=True)
    staff_member = StaffNamesSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = ('user', 'times', 'staff_member')

    def create(self, validated_data):
        times_data = validated_data.pop('times')
        staff = Staff.objects.create(**validated_data)
        for times in times_data:
            delet = TimesRecord.objects.filter(\
                    start_datetime__year=times.get('start_datetime').year,\
                    start_datetime__day=times.get('start_datetime').day,\
                    staff_member=staff).delete()
            print('deleted other time records in create', delet)
            times.pop("staff_member", "");
            new_times = TimesRecord.objects.create(**times, staff_member=staff)
        return staff

    def update(self, instance, validated_data):
        times_data = validated_data.pop('times')
        instance.user = validated_data.get('user', instance.user)
        # for times_instance in instance.times.all():
        #     try:
        #         times = times_data.pop(0)
        #         times_instance.date = times.get('date', times_instance.date)
        #         times_instance.start_datetime = times.get('start_datetime', times_instance.start_datetime)
        #         times_instance.end_datetime = times.get('end_datetime', times_instance.end_datetime)
        #         times_instance.save()
        #     except IndexError:
        #         pass
        for further_times in times_data:
            # todo dont break when now time was added
            delet = TimesRecord.objects \
            .filter(\
                    start_datetime__year=further_times.get('start_datetime').year, \
                    start_datetime__day=further_times.get('start_datetime').day,\
                    staff_member=instance
                ).delete()
            further_times.pop("staff_member", "")
            TimesRecord.objects.create(**further_times, staff_member=instance)
        instance.save()
        return instance

class FullTimesRecordSerializer(serializers.HyperlinkedModelSerializer):
    staff_member = StaffNamesSerializer(read_only=True)
    class Meta:
        model = TimesRecord
        fields = ('id', 'url', 'date', 'start_datetime', 'end_datetime', 'mode', 'staff_member')

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Address
        fields = ('id', 'url', 'street', 'number', 'stair', 'level', 'door', 'extra', 'postal_code', 'customer', 'position', 'lat', 'lon', 'talk_to', 'talk_to_extra')

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    addresses = AddressSerializer(many=True, default=[])
    class Meta:
        model = Customer
        fields = ('id', 'external_id', 'url', 'name', 'phone_1', 'phone_2', 'email', 'payment', 'has_delayed_payment', 'has_delayed_payment_memo', 'addresses')

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses')
        customer = Customer.objects.create(**validated_data)

        for address_data in addresses_data:
            address_data.pop("customer", "") # better save than sorry
            # check if street exists
            print(address_data)
            streetWithNumber = StreetWithNumber.objects.filter(name=address_data.get('street'), nr=address_data.get('number'), postal_code=address_data.get('postal_code'))
            if (streetWithNumber):
                address_data['lat'] = streetWithNumber[0].lat
                address_data['lon'] = streetWithNumber[0].lon
            else:
                    here_maps_api_key = "Up_vTCjQcg2_WoQK79Dlzj6a_MMliPdfYhO0Cvn3kf4"
                    settings = Settings.objects.first()
                    if (here_maps_api_key == ''):
                            print("ERROR: no here maps api key")
                    else:
                        print("get streets from here maps")
                        url = "https://geocode.search.hereapi.com/v1/geocode?at="+str(settings.gps_lat)+","+str(settings.gps_lon)+"&q="+address_data.get('street')+" "+address_data.get('number')+" "+address_data.get('postal_code')+"&lang=de&limit=5&apiKey="+here_maps_api_key
                        print(url)
                        data = requests.get(url)
                        items = data.json()['items']
                        if (len(items) > 0):
                            address_data['lat'] = items[0]['position']['lat']
                            address_data['lon'] = items[0]['position']['lng']
                            StreetWithNumber.objects.create(name=address_data.get('street'), nr=address_data.get('number'), postal_code=address_data.get('postal_code'), lat=address_data['lat'], lon=address_data['lon'])

            Address.objects.update_or_create(customer=customer, **address_data)
        return customer

    def update(self, instance, validated_data):

        addresses = validated_data.pop('addresses')

        instance.phone_1 = validated_data.get('phone_1', instance.phone_1)
        instance.phone_2 = validated_data.get('phone_2', instance.phone_2)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.external_id = validated_data.get('external_id', instance.external_id)
        instance.payment = validated_data.get('payment', instance.payment)
        instance.has_delayed_payment = validated_data.get('has_delayed_payment', instance.has_delayed_payment)
        instance.has_delayed_payment_memo = validated_data.get('has_delayed_payment_memo', instance.has_delayed_payment_memo)
        instance.save()

        for instance_address in instance.addresses.all():
            try:
                address_data = addresses.pop(0)
                instance_address = update_instance_address(instance_address, address_data)
                instance_address.save()
            except IndexError:
                pass
        for further_address_data in addresses:
            if "customer" in address_data:
                address_data.pop("customer")
            Address.objects.create(customer=instance, **further_address_data)
        return instance

class DelayedPaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'url', 'has_delayed_payment', 'has_delayed_payment_memo')
#
class ContractPositionSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer(many=True, default=[])
    customer = CustomerSerializer(read_only=True)
    dispo = DispoSerializer(many=True, read_only=True)
    new_customer = serializers.HyperlinkedRelatedField(view_name = 'customer-detail', write_only=True, queryset=Customer.objects.all(), allow_null=True)
    class Meta:
        model = ContractPosition
        fields = (
            'id',
            'url',
            'position',
            'start_mode',
            'start_time',
            'memo',
            'address',
            'customer',
            'new_customer',
            'anon_name',
            'dispo',
            'weight_size_bonus',
            'distance',
            'zone',
            'is_cargo',
            'is_express',
            'is_bigbuilding',
            'get_there_bonus',
            'waiting_bonus',
            'price',
            'bonus',
            'phone_1',
            'email',
            'talk_to'
        )
        extra_kwargs = {
            'start_mode': {
                # Tell DRF that the link field is not required.
                'required': False,
                'allow_blank': True,
            }
        }

    def create(self, validated_data):
        return create_new_position(validated_data)

    def update(self, instance, validated_data):
        instance = update_position(instance, validated_data)
        instance.save()
        return instance


class StreetSerializer(serializers.Serializer):
    name = serializers.CharField()
    name_street = serializers.CharField()
    nr_von = serializers.CharField()
    nr_bis = serializers.CharField()
    lon = serializers.FloatField()
    lat = serializers.FloatField()
    postal_code = serializers.CharField()

class RepeatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repeated
        fields = ('contract', 'start_date', 'end_date', 'movable_date', 'days_of_the_week')

class ArchiveDispoSerializer(serializers.ModelSerializer):
    dispatched_to = StaffNamesSerializer(read_only=True)
    class Meta:
        model = Dispo
        fields = ('url', 'created', 'contract', 'dispatched_to', 'sequence', 'position', 'preliminary')

class ArchivePositionSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer(read_only=True, many=True, default=[])
    customer = CustomerSerializer(read_only=True)
    dispo = ArchiveDispoSerializer(many=True, read_only=True)
    class Meta:
        model = ContractPosition
        fields = (
            'id',
            'url',
            'position',
            'start_mode',
            'start_time',
            'memo',
            'address',
            'customer',
            'anon_name',
            'dispo',
            'weight_size_bonus',
            'distance',
            'zone',
            'is_cargo',
            'is_express',
            'is_bigbuilding',
            'get_there_bonus',
            'waiting_bonus',
            'price',
            'bonus',
            'phone_1',
            'email',
            'talk_to'
        )

class ArchiveContractSerializer(serializers.HyperlinkedModelSerializer):
    positions = ArchivePositionSerializer(many=True, read_only=True)
    class Meta:
        model = Contract
        fields = ('id',
                  'url',
                  'created',
                  'zone',
                  'distance',
                  'price',
                  'extra',
                  'customer',
                  'positions',
                  'type')

class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Settings
        fields = "__all__"


class ContractSerializer(serializers.HyperlinkedModelSerializer):
    positions = ContractPositionSerializer(many=True, default=[])
    repeated = RepeatedSerializer(default=None, allow_null=True)
    # dispo = serializers.HyperlinkedRelatedField(many=True, view_name='dispo-detail', queryset=Dispo.objects.all())
    class Meta:
        model = Contract
        fields = ('id',
                  'url',
                  'created',
                  'zone',
                  'distance',
                  'price',
                  'extra',
                  'customer',
                  'positions',
                  'type',
                  'repeated',
                  'fromrepeated'
                    )

    def create(self, validated_data):

        customer = validated_data.pop('customer', None)
        positions = validated_data.pop('positions', [])
        repeated = validated_data.pop('repeated', None)
        dispo = validated_data.pop('dispo', [])

        contract = Contract.objects.create(**validated_data, customer = customer)

        for position in positions:
            newPosition = create_new_position(position, contract=contract)

        create_new_repeated(repeated, contract=contract)

        contract.save()
        return contract

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions', [])

        instance.zone = validated_data.get('zone', instance.zone)
        instance.distance = validated_data.get('distance', instance.distance)
        instance.price = validated_data.get('price', instance.price)
        instance.extra = validated_data.get('extra', instance.extra)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.type = validated_data.get('type', instance.type)
        instance.save()

        if hasattr(instance, 'repeated'):
            repeated_instance = update_repeated(instance.repeated, validated_data)
        elif (validated_data.get('repeated')):
            Repeated.objects.create(**validated_data.get('repeated'), contract=instance)

        for instance_position in instance.positions.all():
            try:
                position_data = positions.pop(0)
                instance_position = update_position(instance_position, position_data)
                instance_position.save()
            except IndexError:
                pass

        for further_position_data in positions:
            create_new_position(further_position_data, contract=instance)

        return instance