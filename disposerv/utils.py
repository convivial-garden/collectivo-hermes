from datetime import timezone
import datetime
import logging
from celery import shared_task

from django.http import HttpResponse

from .models import Contract, RepeatedContract

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
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug("###########################################################")
    logger.debug("DEBUG ----------- generateRepeatedContracts ---------------")
    logger.debug("###########################################################")

    repeated_contracts = RepeatedContract.objects \
            .filter(
        Q(repeated__end_date__gt=timezone.now()) | Q(repeated__end_date__isnull=True),
        Q(repeated__movable_date__lt=timezone.now()) | Q(repeated__movable_date__isnull=True),
            repeated__start_date__lt=timezone.now()).order_by('id')

    for contract in repeated_contracts:
        logger.debug("Contract ID {}".formxat(contract.id))
        # if contract.repeated.movable_date == None:
        logger.debug("generating contracts until end of week")
        current_date = datetime.datetime.today().replace(tzinfo=pytz.UTC)
        logger.debug("start date {}".format(current_date))
        contract.repeated.movable_date = contract.repeated.start_date.replace(tzinfo=pytz.UTC)
        logger.debug("movable_date date {}".format(contract.repeated.movable_date))
        days_til_monday = 7 - current_date.weekday()
        one_past_end_date = current_date + datetime.timedelta(days=(days_til_monday))
        logger.debug("one past end date {}".format(one_past_end_date))
        assert (one_past_end_date.weekday() == 0)
        while current_date != one_past_end_date:
            logger.debug("days of the week {}".format(contract.repeated.days_of_the_week))
            if WEEKDAYS[current_date.weekday()] in contract.repeated.days_of_the_week:
                cd= timezone.make_aware(datetime.datetime.combine(current_date, datetime.datetime.min.time()))
                logger.debug("date for contract {}".format(cd))
                # check if contract already exists
                if not Contract.objects.filter(repeated_id=contract.repeated.id, created=cd).exists():
                    generateContractFromRepeatedContract(cd, contract)
                else: 
                    logger.debug("contract already exists")
            current_date = current_date + datetime.timedelta(days=1)
        contract.repeated.movable_date = contract.repeated.movable_date + datetime.timedelta(days_til_monday)
        logger.debug("movable date {}".format(contract.repeated.movable_date))
        contract.repeated.save()
    logger.debug("###########################################################")
    logger.debug("END DEBUG ----------- generateRepeatedContracts -----------")
    logger.debug("###########################################################")
    return HttpResponse("OK1")


def generateContractFromRepeatedContract(current_date, cntrct):
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
    cntrct.id = None
    cntrct.save()
    # tz = pytz.timezone('Europe/Vienna')
    dt = current_date
    cntrct.created = dt
    cntrct.fromrepeated = True
    cntrct.repeated_id = repeated_id
    cntrct.save()
    for position in all_positions:
        position_address = position.address.all()[0]
        position.id = None
        position.contract = cntrct
        position.start_time = datetime.datetime.combine(current_date, position.start_time.time()).replace(tzinfo=pytz.UTC)
        position.save()
        logger.debug("Generated position {}".format(position.id))
        position_address.id = None
        position_address.position = position
        position_address.save()
        logger.debug("Generated position {}".format(position_address.id, position.start_time))
    logger.debug("generateContractFromRepeatedContract {}".format(current_date.isoformat()))
    return HttpResponse("OK2")