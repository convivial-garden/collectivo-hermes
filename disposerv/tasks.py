from celery import shared_task

@shared_task(name="my_extension_task")
def my_extension_task():
    print("my_extension_task has been called")
