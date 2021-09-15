from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count()


bind = '0.0.0.0:' + environ.get('PORT', '7004')
max_requests = 1000
worker_class = "aiohttp.worker.GunicornWebWorker"
workers = max_workers()


reload = True
name = 'webcam69'
