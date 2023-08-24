from datetime import *
from django.utils import timezone
import logging
from celery import shared_task
from django.db.models import Q
import pytz


from django.http import HttpResponse

from .models import Contract, ContractPosition, PositionAddress, RepeatedContract, RepeatedContractForDate

WEEKDAYS = {
    0 : 'Monday'   ,
    1 : 'Tuesday'  ,
    2 : 'Wednesday',
    3 : 'Thursday' ,
    4 : 'Friday'   ,
    5 : 'Saturday' ,
    6 : 'Sunday'   ,
}


@shared_task(name="generateRepeatedContracts")
def generateRepeatedContracts(req):
    try:
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.debug("###########################################################")
        logger.debug("DEBUG ----------- generateRepeatedContracts3 ---------------")
        logger.debug("###########################################################")

        repeated_contracts = RepeatedContract.objects \
                .filter(
            Q(repeated__end_date__gt=timezone.now()) | Q(repeated__end_date__isnull=True),
                repeated__start_date__lt=timezone.now()).order_by('id')
        len_repeated_contracts = len(repeated_contracts)
        print("len_repeated_contracts {}".format(len_repeated_contracts))
        for contract in repeated_contracts:
            logger.debug("Contract ID {}".format(contract.id))
            logger.debug("generating contracts until end of week")
            current_date = datetime.today().replace(tzinfo=pytz.UTC)
            logger.debug("start date {}".format(current_date))
            one_past_end_date = current_date + timedelta(days=(7))
            logger.debug("one past end date {}".format(one_past_end_date))
            while current_date != one_past_end_date:
                logger.debug("days of the week {}".format(contract.repeated.days_of_the_week))
                if WEEKDAYS[current_date.weekday()] in contract.repeated.days_of_the_week:
                    cd= timezone.make_aware(datetime.combine(current_date, datetime.min.time()))
                    logger.debug("date for contract {}".format(cd))
                    # check if contract already exists
                    if not RepeatedContractForDate.objects.filter(repeated=contract.repeated.id, date=cd).exists():
                        generateContractFromRepeatedContract(cd, contract)
                    else: 
                        logger.debug("contract already exists")
                current_date = current_date + timedelta(days=1)
            contract.repeated.save()
        logger.debug("###########################################################")
        logger.debug("END DEBUG ----------- generateRepeatedContracts -----------")
        logger.debug("###########################################################")
    except Exception as e:
        logger.debug("Exception {}".format(e))


def generateContractFromRepeatedContract(current_date, cntrct):
    try:
        logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.debug("###########################################################")
        logger.debug("DEBUG ----------- generateContractFromRepeatedContract ---------------")
        logger.debug("###########################################################")
        logger.debug("Generate a contract on {} for repeadted contract".format(WEEKDAYS[current_date.weekday()]))
        all_positions = cntrct.positions.all()
        logger.debug("positions {}".format(all_positions))
        repeated_id = cntrct.repeated.id
        new_contract = Contract()
        # tz = pytz.timezone('Europe/Vienna')
        dt = current_date
        new_contract.created = dt
        new_contract.fromrepeated = True
        new_contract.repeated_id = repeated_id
        new_contract.customer = cntrct.customer
        new_contract.zone = cntrct.zone
        new_contract.distance = cntrct.distance
        new_contract.price = cntrct.price
        new_contract.extra = cntrct.extra
        new_contract.type = cntrct.type
        new_contract.fromrepeated = True
        new_contract.repeated_deleted = cntrct.repeated_deleted
        new_contract.save()
        print("new contract {}".format(new_contract.id))
        for position in all_positions:
            position_address = position.address.all()[0]
            new_position_address = PositionAddress()
            new_position_address.customer = position_address.customer
            new_position_address.street = position_address.street
            new_position_address.number = position_address.number
            new_position_address.stair = position_address.stair
            new_position_address.level = position_address.level
            new_position_address.door = position_address.door
            new_position_address.extra = position_address.extra
            new_position_address.postal_code = position_address.postal_code
            new_position_address.talk_to = position_address.talk_to
            new_position_address.talk_to_extra = position_address.talk_to_extra
            new_position_address.opening_hours = position_address.opening_hours
            new_position_address.lat = position_address.lat
            new_position_address.lon = position_address.lon
            new_position = ContractPosition()
            new_position.customer = position.customer
            new_position.customer_is_pick_up = position.customer_is_pick_up
            new_position.customer_is_drop_off = position.customer_is_drop_off
            print("position.start_time {}".format(position.start_time))
            print("current_date {}".format(current_date))
            print("combined")
            new_position.start_time = datetime.combine(current_date, position.start_time.time()).replace(tzinfo=pytz.UTC)
            new_position.start_time_to =datetime.combine(current_date, position.start_time_to.time()).replace(tzinfo=pytz.UTC)
            new_position.end_time_from = position.end_time_from
            new_position.end_time = position.end_time
            new_position.contract = new_contract

            new_position.weight_size_bonus = position.weight_size_bonus
            new_position.is_cargo = position.is_cargo
            new_position.is_express = position.is_express
            new_position.is_bigbuilding = position.is_bigbuilding
            new_position.get_there_bonus = position.get_there_bonus
            new_position.waiting_bonus = position.waiting_bonus
            new_position.memo = position.memo
            new_position.distance = position.distance
            new_position.price = position.price
            new_position.bonus = position.bonus
            new_position.storage = position.storage
            new_position.zone = position.zone
            new_position.phone_1 = position.phone_1
            new_position.email = position.email
            new_position.talk_to = position.talk_to

            

            new_position.save()
            new_position_address.position = new_position
            new_position_address.save()
            logger.debug("Generated position {}".format(new_position.id))
            RepeatedContractForDate.objects.create(repeated = cntrct.repeated, contract = new_contract, date = dt, created = True)
            logger.debug("Generated position {}".format(position_address.id, position.start_time))
        logger.debug("generateContractFromRepeatedContract {}".format(current_date.isoformat()))
    except Exception as e:
        logger.debug("Exception {}".format(e))