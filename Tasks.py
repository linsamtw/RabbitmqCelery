
import os, sys
PATH = '/'.join( os.path.abspath(__file__).split('/')[:-1] )
sys.path.append(PATH)
from Worker import app
@app.task()
def add(x,y):
    return x+y

