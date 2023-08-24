from django.db import models
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords
from django.db.models import signals


class Customer(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    external_id = models.IntegerField(default='-1')
    phone_1 = models.CharField(max_length=100, blank=True)
    phone_2 = models.CharField(max_length=100, blank=True)
    email = models.CharField(blank=True, max_length=300)
    name = models.CharField(max_length=200)
    payment = models.CharField(max_length=10, default='Bar')
    has_delayed_payment = models.BooleanField(default=False)
    has_delayed_payment_memo = models.TextField(blank=True, default='')
    memo = models.TextField(blank=True)
    is_blacklisted = models.BooleanField(default=False)
    is_blacklisted_memo = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('added',)

    def __str__(self):
        return self.name

class GenericAddress(models.Model):
    customer = models.ForeignKey(Customer, related_name="addresses",on_delete=models.SET_NULL, null=True, blank=True)
    street = models.CharField(max_length=300, default='', blank=True)
    number = models.CharField(max_length=10, blank=True)
    stair = models.CharField(max_length=10, blank=True)
    level = models.CharField(max_length=10, blank=True)
    door = models.CharField(max_length=10, blank=True)
    extra = models.CharField(max_length=300, blank=True)
    postal_code = models.CharField(max_length=6, blank=True)
    talk_to = models.CharField(max_length=400,blank=True, default='')
    talk_to_extra = models.CharField(max_length=400, blank=True, default='')
    opening_hours = models.CharField(max_length=300, blank=True)
    lat = models.FloatField(null=True, default=48.216618)
    lon = models.FloatField(null=True, default=16.385031)

    def __str__(self):
        return self.street + ' ' + self.number
class PositionAddress(GenericAddress):
    position = models.ForeignKey('ContractPosition', related_name="address",on_delete=models.SET_NULL, null=True, blank=True)
    pass
class RepeatedPositionAddress(GenericAddress):
    position = models.ForeignKey('RepeatedContractPosition', related_name="address",on_delete=models.SET_NULL, null=True, blank=True)
    pass

class Street(models.Model):
    name = models.CharField(max_length=400, default='')
    name_street = models.CharField(max_length=400, default='')
    nr_von = models.CharField(max_length=10, null=True)
    nr_bis = models.CharField(max_length=10, null=True)
    postal_code = models.CharField(max_length=4)
    lat = models.FloatField(default=16)
    lon = models.FloatField(default=48)

    class Meta:
        indexes = [
            models.Index(
                fields=['name', 'name_street', 'nr_von', 'nr_bis'])
        ]
class StreetWithNumber(models.Model):
    name = models.CharField(max_length=400, default='')
    nr = models.CharField(max_length=10, null=True)
    postal_code = models.CharField(max_length=4)
    lat = models.FloatField(default=16)
    lon = models.FloatField(default=48)

    class Meta:
        indexes = [
            models.Index(
                fields=['name', 'nr'])
        ]
class AddressPosition(models.Model):
    address = models.ForeignKey(PositionAddress, related_name="positions",on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey('ContractPosition', related_name="addressposition",on_delete=models.SET_NULL, null=True, blank=True)
    lat = models.FloatField(null=True, default=48.216618)
    lon = models.FloatField(null=True, default=16.385031)

class AddressReapeatedPosition(models.Model):
    address = models.ForeignKey(RepeatedPositionAddress, related_name="positions",on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey('RepeatedContractPosition', related_name="addressposition",on_delete=models.SET_NULL, null=True, blank=True)
    lat = models.FloatField(null=True, default=48.216618)
    lon = models.FloatField(null=True, default=16.385031)


class Staff(models.Model):
    """An extension of the user model with dispo staff data."""
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="disposerv_profile",
        primary_key=True
    ) 
    isDispo = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        """Return a string representation of the object."""
        return str(self.user)
    
    def find_or_create_user(sender, instance, **kwargs):
        staff, created = Staff.objects.update_or_create(user=instance)
        if created:
            Staff.objects.create(user=instance)

class TimesRecord(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    mode = models.CharField(max_length=10, default='fahrer')
    staff_member = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True, related_name="times")

    class Meta:
        indexes = [
            models.Index(fields=['date', 'start_datetime', 'end_datetime', 'mode', 'staff_member'])
        ]

    def __str__(self):
        return "Stunden von " + repr(self.staff_member) + " am " + str(self.date)

class Contract(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)
    zone = models.PositiveIntegerField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    extra = models.FloatField(null=True)
    type = models.CharField(max_length=100, default='einzelfahrt')
    fromrepeated = models.BooleanField(blank=True,default=False)
    repeated_id = models.PositiveIntegerField(blank=True, null=True)
    repeated_deleted = models.BooleanField(blank=True,default=False, null=True)

    def __str__(self):
        return 'Auftragnummer ' + str(self.id)

class GenericPosition(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='customer', db_constraint=False)
    customer_is_pick_up = models.BooleanField(default=True)
    customer_is_drop_off = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    start_time= models.DateTimeField(blank=True, null=True)
    start_time_to = models.DateTimeField(blank=True, null=True)
    end_time_from = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    anon_name = models.CharField(max_length=300, default='', blank=True)

    weight_size_bonus = models.CharField(max_length=10, default='', blank=True)
    is_cargo = models.BooleanField(default=False)
    is_express = models.BooleanField(default=False)
    is_bigbuilding = models.BooleanField(default=False)
    get_there_bonus = models.FloatField(default=0.)
    waiting_bonus = models.IntegerField(default=0)
    memo = models.TextField(blank=True)
    distance = models.FloatField(null=True, default=0.)
    price = models.FloatField(default=0.)
    bonus = models.FloatField(default=0.)
    storage = models.BooleanField(default=False)
    zone = models.IntegerField(null=True, default=1)
    phone_1 = models.CharField(max_length=300, default='', blank=True)
    email = models.CharField(max_length=300, default='', blank=True)
    talk_to = models.CharField(max_length=400, default='', blank=True)

    def __str__(self):
        return 'id ' + str(self.id)

    class Meta:
        indexes = [
            models.Index(fields=['start_time'])
        ]
class RepeatedContract(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)
    zone = models.PositiveIntegerField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    extra = models.FloatField(null=True)
    type = models.CharField(max_length=100, default='einzelfahrt')
    fromrepeated = models.BooleanField(blank=True,default=False)
    repeated_id = models.PositiveIntegerField(blank=True, null=True)
    repeated_deleted = models.BooleanField(blank=True,default=False, null=True)

class ContractPosition(GenericPosition):
    contract = models.ForeignKey(Contract, related_name='positions', on_delete=models.CASCADE, blank=True, null=True)
    pass

class RepeatedContractPosition(GenericPosition):
    contract = models.ForeignKey(RepeatedContract, related_name='positions', on_delete=models.CASCADE, blank=True, null=True)
    pass

# user own models for repeated orders


class Repeated(models.Model):
    contract = models.OneToOneField(RepeatedContract, on_delete=models.CASCADE, null=True, related_name='repeated')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    days_of_the_week = models.CharField(max_length=60, blank=True)
    notes = models.TextField(blank=True)

class RepeatedContractForDate(models.Model):
    repeated = models.ForeignKey(Repeated, on_delete=models.SET_NULL, null=True, related_name='repeatedcontracts')
    date = models.DateTimeField()
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, related_name='repeatedcontracts')
    created = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    changed = models.BooleanField(default=False)

class Dispo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True, null=True)
    dispatched_to = models.ForeignKey(Staff, on_delete=models.CASCADE, default=0)
    sequence = models.PositiveIntegerField(default=0)
    position = models.ForeignKey(ContractPosition, on_delete=models.CASCADE, related_name='dispo', default=0)
    preliminary = models.BooleanField(default=False)

class Settings(models.Model):
    basezone_price = models.FloatField(default=8.)
    addzone_price = models.FloatField(default=4.)
    express_price = models.FloatField(default=4.)
    express_price_zone_size = models.IntegerField(default=2)
    zone_size = models.FloatField(default=3.)
    addzone_size =  models.FloatField(default=2.)
    city = models.CharField(max_length=100, default='Wien')
    gps_lat = models.FloatField(default=48.216618)
    gps_lon = models.FloatField(default=16.385031)

def update_disposerv_user(sender, instance, created, **kwargs):
    """Create or update related keycloak user when a django user is changed."""
    print("update_disposerv_user")
    Staff.find_or_create_user(sender, instance)


# signals.post_save.connect(
#     update_disposerv_user,
#     sender=get_user_model(),
#     dispatch_uid="update_disposerv_user",
#     weak=False,
# )