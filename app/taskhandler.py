from app import celery

@celery.task
def hardtask(current_user,abook):
    pass