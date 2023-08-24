from celery import shared_task
from .utils import generateRepeatedContracts

@shared_task(name="disposerv-repeated-contracts")
def disposerv_repeated_contracts():
    print("disposerv has been called2")
    generateRepeatedContracts(None)
