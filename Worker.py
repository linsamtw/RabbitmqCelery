

import os, sys
PATH = '/'.join( os.path.abspath(__file__).split('/')[:-1] )
sys.path.append(PATH)
from celery import Celery
app = Celery("task",
             include=["Tasks"],
             broker='pyamqp://worker:worker@localhost:5672/')


