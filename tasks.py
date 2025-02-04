from celery.bin import worker
from bankr.tasks import celery

options = {'loglevel': 'INFO'}

if __name__ == '__main__':
    worker = worker.worker(app=celery)
    worker.run(**options)
